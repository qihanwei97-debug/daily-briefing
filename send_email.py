"""
晨报邮件发送器
读取仓库中最新的晨报 .md 文件，转为 HTML 邮件发送给收件人。
由 GitHub Actions 在收到新晨报文件后自动触发。
"""

import smtplib
import os
import sys
import re
import glob
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ============ 配置（从 GitHub Secrets 读取） ============

RECIPIENTS = os.environ.get("RECIPIENTS", "").split(",")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))


# ============ 找到最新的晨报文件 ============

def find_latest_briefing():
    """找到 briefings/ 目录下最新的晨报 .md 文件"""
    files = glob.glob("briefings/晨报_*.md")
    if not files:
        print("错误：briefings/ 目录下没有找到晨报文件")
        sys.exit(1)

    # 按文件名排序，取最新的
    files.sort(reverse=True)
    latest = files[0]
    print(f"找到最新晨报: {latest}")
    return latest


# ============ Markdown → HTML 邮件 ============

def markdown_to_html(md_text):
    """将 Markdown 转为美观的 HTML 邮件格式"""
    html = md_text

    # 先提取链接，用占位符保护 URL 不被转义
    links = []
    def _save_link(m):
        idx = len(links)
        links.append((m.group(1), m.group(2)))
        return f"\x00LINK{idx}\x00"
    html = re.sub(r"\[(.+?)\]\((.+?)\)", _save_link, html)

    # 提取行内代码，用占位符保护
    codes = []
    def _save_code(m):
        idx = len(codes)
        codes.append(m.group(1))
        return f"\x00CODE{idx}\x00"
    html = re.sub(r"`(.+?)`", _save_code, html)

    # 转义 HTML 特殊字符
    html = html.replace("&", "&amp;")
    html = html.replace("<", "&lt;")
    html = html.replace(">", "&gt;")

    # 还原链接和代码
    for i, (text, url) in enumerate(links):
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        html = html.replace(f"\x00LINK{i}\x00", f'<a href="{url}" style="color:#0066cc;">{text}</a>')
    for i, code in enumerate(codes):
        code = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        html = html.replace(f"\x00CODE{i}\x00", f'<code style="background:#f0f0f0;padding:2px 5px;border-radius:3px;font-size:90%;">{code}</code>')

    # 标题
    html = re.sub(r"^####\s+(.+)$", r"<h4 style='color:#1a1a1a;margin:18px 0 8px;'>\1</h4>", html, flags=re.MULTILINE)
    html = re.sub(r"^###\s+(.+)$", r"<h3 style='color:#1a1a1a;margin:20px 0 10px;'>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"^##\s+(.+)$", r"<h2 style='color:#2c2c2c;border-bottom:1px solid #eee;padding-bottom:6px;margin:24px 0 12px;'>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^#\s+(.+)$", r"<h1 style='color:#000;margin:0 0 16px;'>\1</h1>", html, flags=re.MULTILINE)

    # 粗体和斜体
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html)

    # 表格处理
    lines = html.split("\n")
    in_table = False
    result_lines = []

    for line in lines:
        stripped = line.strip()
        if "|" in stripped and stripped.startswith("|"):
            if re.match(r"^\|[\s\-:|]+\|$", stripped):
                continue
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if not in_table:
                result_lines.append('<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;font-size:13px;margin:12px 0;">')
                row = "<tr>" + "".join(f"<th style='background:#f8f8f8;padding:8px 10px;text-align:left;font-weight:600;'>{c}</th>" for c in cells) + "</tr>"
                in_table = True
            else:
                row = "<tr>" + "".join(f"<td style='padding:8px 10px;vertical-align:top;'>{c}</td>" for c in cells) + "</tr>"
            result_lines.append(row)
        else:
            if in_table:
                result_lines.append("</table>")
                in_table = False
            if stripped == "---":
                result_lines.append("<hr style='border:none;border-top:1px solid #ddd;margin:20px 0;'>")
            elif stripped == "":
                result_lines.append("")
            elif stripped.startswith("- "):
                result_lines.append(f"<p style='margin:4px 0 4px 16px;'>{stripped}</p>")
            elif not stripped.startswith("<h") and not stripped.startswith("<table") and not stripped.startswith("<hr"):
                result_lines.append(f"<p style='margin:6px 0;'>{stripped}</p>")
            else:
                result_lines.append(stripped)

    if in_table:
        result_lines.append("</table>")

    body = "\n".join(result_lines)

    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; max-width: 820px; margin: 0 auto; padding: 24px; color: #333; line-height: 1.7; background: #fff;">
{body}
</body>
</html>"""


# ============ 发送邮件 ============

def send_email(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        briefing_text = f.read()

    # 从文件名提取日期作为邮件标题
    filename = os.path.basename(filepath)
    # 匹配 "晨报_2026年02月28日.md"
    date_match = re.search(r"(\d{4}年\d{2}月\d{2}日)", filename)
    date_str = date_match.group(1) if date_match else "今日"
    subject = f"AI 日报 | {date_str}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(RECIPIENTS)

    # 纯文本版本
    text_part = MIMEText(briefing_text, "plain", "utf-8")
    msg.attach(text_part)

    # HTML 版本
    html_content = markdown_to_html(briefing_text)
    html_part = MIMEText(html_content, "html", "utf-8")
    msg.attach(html_part)

    print(f"正在发送邮件: {subject}")
    print(f"收件人: {RECIPIENTS}")

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SMTP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENTS, msg.as_string())

    print("邮件发送成功！")


# ============ 主函数 ============

def main():
    missing = []
    if not SENDER_EMAIL:
        missing.append("SENDER_EMAIL")
    if not SMTP_PASSWORD:
        missing.append("SMTP_PASSWORD")
    if not RECIPIENTS or RECIPIENTS == [""]:
        missing.append("RECIPIENTS")

    if missing:
        print(f"错误：缺少环境变量: {', '.join(missing)}")
        sys.exit(1)

    filepath = find_latest_briefing()
    send_email(filepath)
    print("完成！")


if __name__ == "__main__":
    main()
