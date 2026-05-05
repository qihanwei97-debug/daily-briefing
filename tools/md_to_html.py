#!/usr/bin/env python3
"""
将晨报 Markdown 转换为带样式的 HTML（5 板块结构）。

用法：
    python tools/md_to_html.py briefings/晨报_2026年04月27日.md
    输出至 briefings/html/2026-04-27.html
"""

import sys
import re
import os
from pathlib import Path

CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
  color: #2d2a26;
  background: #f0eeeb;
  line-height: 1.8;
  -webkit-font-smoothing: antialiased;
}
.page {
  max-width: 640px;
  margin: 0 auto;
  background: #fff;
  min-height: 100vh;
  padding: 0 28px;
}
a { color: #2563eb; text-decoration: none; }
a:hover { text-decoration: underline; }

.masthead {
  padding: 36px 0 20px;
  border-bottom: 1px solid #eae7e2;
  position: relative;
  overflow: hidden;
}
.masthead::before {
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 180px; height: 100%;
  background: linear-gradient(135deg, transparent 40%, rgba(37,99,235,0.03) 100%);
}
.masthead .en {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 4px;
  color: #b5ada4;
  text-transform: uppercase;
  margin-bottom: 4px;
  position: relative;
}
.masthead h1 {
  font-size: 28px;
  font-weight: 800;
  letter-spacing: 2px;
  color: #1a1a2e;
  margin-bottom: 10px;
  position: relative;
}
.masthead h1 .ai { color: #2563eb; }
.masthead .gold-line {
  width: 32px; height: 3px;
  background: #c9a96e;
  border-radius: 2px;
  margin-bottom: 12px;
}
.masthead .meta {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #b5ada4;
  position: relative;
}

.sec-title {
  font-size: 17px;
  font-weight: 700;
  color: #2d2a26;
  padding-left: 14px;
  border-left: 3px solid #2563eb;
  margin-bottom: 18px;
}

.sep {
  border: none;
  border-top: 1px solid #eae7e2;
  margin: 36px 0 28px;
}

.summary { margin-bottom: 0; }
.summary ul { list-style: none; }
.summary li {
  font-size: 14px;
  line-height: 1.8;
  padding: 12px 0;
  border-bottom: 1px solid #f2efeb;
}
.summary li:last-child { border-bottom: none; }
.summary li strong { color: #1a1a2e; font-weight: 600; }
.summary .aside { color: #9a938a; font-size: 13px; }

.feature { margin-bottom: 28px; }
.feature h3 {
  font-size: 18px;
  font-weight: 700;
  line-height: 1.5;
  color: #1a1a2e;
  margin-bottom: 14px;
}
.feature p {
  font-size: 15px;
  margin-bottom: 12px;
  color: #3d3832;
}
.callout {
  border-left: 3px solid #c9a96e;
  padding: 14px 18px;
  margin: 16px 0;
  font-size: 14px;
  line-height: 1.85;
  background: #fffdf9;
}
.callout strong { color: #2d2a26; font-weight: 700; }
.callout-intro { margin-bottom: 10px; }
.callout-list {
  list-style: none;
  padding: 0;
  margin: 0;
  counter-reset: callout-item;
}
.callout-list li {
  position: relative;
  padding: 8px 0 8px 28px;
  border-bottom: 1px solid #f3eadb;
  counter-increment: callout-item;
}
.callout-list li:last-child { border-bottom: none; padding-bottom: 0; }
.callout-list li::before {
  content: counter(callout-item);
  position: absolute;
  left: 0;
  top: 8px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #c9a96e;
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  text-align: center;
  line-height: 20px;
}
.link-cluster {
  display: block;
  font-size: 12px;
  color: #b5ada4;
  line-height: 1.7;
  margin-top: 6px;
  padding-left: 18px;
  position: relative;
}
.link-cluster::before {
  content: '📚';
  position: absolute;
  left: 0;
  font-size: 11px;
}
.link-cluster a { color: #9a938a; }
.link-cluster a:hover { color: #2563eb; }
.sources {
  font-size: 12px;
  color: #b5ada4;
  margin-top: 14px;
  line-height: 1.8;
}

.brief-item {
  padding: 18px 0;
  border-bottom: 1px solid #f2efeb;
}
.brief-item:last-child { border-bottom: none; }
.brief-item h4 {
  font-size: 15px;
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 6px;
}
.brief-item p {
  font-size: 14px;
  color: #4a4540;
}
.brief-item .insight {
  font-size: 13px;
  color: #5a5550;
  margin-top: 8px;
  padding-left: 14px;
  border-left: 2px solid #c9a96e;
  line-height: 1.75;
}

.product-table { margin: 8px 0; }
.product-table table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}
.product-table th {
  background: #faf9f7;
  padding: 10px 8px;
  text-align: left;
  font-weight: 600;
  border-bottom: 1px solid #eae7e2;
  color: #5a5550;
}
.product-table td {
  padding: 10px 8px;
  border-bottom: 1px solid #f2efeb;
  vertical-align: top;
}

.changes ul { list-style: none; padding: 0; }
.changes li {
  font-size: 14px;
  line-height: 1.85;
  padding: 4px 0;
}
.changes strong { color: #1a1a2e; }

.tip h3 {
  font-size: 16px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 14px;
  line-height: 1.55;
}
.tip p {
  font-size: 14px;
  color: #3d3832;
  margin-bottom: 12px;
  line-height: 1.9;
}
.tip strong { color: #1a1a2e; }
.tip ol, .tip ul {
  background: #faf9f7;
  border: 1px solid #eae7e2;
  border-radius: 4px;
  padding: 14px 16px 14px 32px;
  font-size: 14px;
  line-height: 1.9;
  margin: 12px 0;
}
.tip li { padding: 2px 0; }

.footer {
  padding: 28px 0;
  font-size: 12px;
  color: #b5ada4;
  text-align: center;
  line-height: 1.8;
  border-top: 1px solid #eae7e2;
  margin-top: 36px;
}

@media (max-width: 640px) {
  .page { max-width: 100%; padding: 0 22px; }
  .masthead { padding: 28px 0 16px; }
  .feature h3 { font-size: 17px; }
  .product-table table { font-size: 12px; }
}
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>每日AI简报 | {date}</title>
<style>{css}</style>
</head>
<body>
<div class="page">
{masthead}
{body}
<div class="footer">{footer}</div>
</div>
</body>
</html>
"""


def render_inline(text: str) -> str:
    """渲染 markdown 行内元素：**bold**、[text](url)、——dash"""
    # 链接 [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # 粗体 **text**
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    return text


def fold_link_clusters(html: str) -> str:
    """折叠段内密集链接：（[A](u1) | [B](u2) | [C](u3) ...）≥3 个时压缩成视觉淡化的 📚 来源块。

    输入是已 render_inline 后的 HTML 片段；只对 <a> 链接族操作，不破坏其他内容。
    """
    pattern = r'（\s*((?:<a[^>]*>[^<]+</a>\s*\|\s*){2,}<a[^>]*>[^<]+</a>)\s*）'
    return re.sub(pattern, r'<span class="link-cluster">\1</span>', html)


def split_callout_circled(content: str) -> tuple:
    """如果 callout 内含 ①②③④⑤⑥⑦⑧⑨⑩ 子点，拆出 (intro, [items])。
    若无环形数字标记，返回 (None, None) 表示按整段渲染。
    """
    if not re.search(r'[①②③④⑤⑥⑦⑧⑨⑩]', content):
        return None, None
    first = re.search(r'[①②③④⑤⑥⑦⑧⑨⑩]', content)
    intro = content[:first.start()].strip()
    list_text = content[first.start():]
    items = re.split(r'(?=[①②③④⑤⑥⑦⑧⑨⑩])', list_text)
    items = [re.sub(r'^[①②③④⑤⑥⑦⑧⑨⑩]\s*', '', x).strip().rstrip('；;。') for x in items if x.strip()]
    return intro, items


def parse_metadata(md: str) -> dict:
    """提取标题、日期、覆盖时间、阅读时间。"""
    m = re.search(r'^\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|\s*(.+?)$', md, re.M)
    if m:
        return {
            'date': m.group(1).strip(),
            'coverage': m.group(2).strip(),
            'reading': m.group(3).strip(),
        }
    return {'date': '', 'coverage': '', 'reading': ''}


def split_sections(md: str) -> list:
    """按 ## H2 切分板块。返回 [(title, content)]。"""
    # 移除报头部分（第一个 ## 之前的所有内容）
    parts = re.split(r'\n## ', md)
    if len(parts) < 2:
        return []
    sections = []
    for chunk in parts[1:]:
        lines = chunk.split('\n', 1)
        title = lines[0].strip()
        content = lines[1] if len(lines) > 1 else ''
        sections.append((title, content.strip()))
    return sections


def render_summary(content: str) -> str:
    """渲染 60 秒速览（bullet 列表）。"""
    items = re.findall(r'^- (.+?)(?=\n- |\n---|\n##|\Z)', content, re.M | re.S)
    html = '<div class="summary"><ul>'
    for item in items:
        item = item.strip().replace('\n', ' ')
        # 把 ——xxx 部分改成 <span class="aside">
        item = re.sub(r'——(.+?)$', r'<span class="aside">——\1</span>', item)
        html += f'<li>{render_inline(item)}</li>'
    html += '</ul></div>'
    return html


def render_deep_report(content: str) -> str:
    """渲染深度报道（头条 + 速报）。"""
    html = ''

    # 用 ### 分割头条与速报
    blocks = re.split(r'\n### ', content)
    for i, block in enumerate(blocks):
        block = block.strip()
        if not block:
            continue
        # 第一行是标题，余下是正文
        lines = block.split('\n', 1)
        title = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ''

        if '速报' in title or '📡' in title:
            html += render_briefs(body)
        else:
            html += render_headline(title, body)
    return html


def render_headline(title: str, body: str) -> str:
    """渲染单条头条（含 callout 和 sources）。"""
    # 清理 markdown ### 前缀（split 没切干净的首块）
    title = re.sub(r'^#+\s*', '', title)
    # 清理 emoji 前缀
    title = re.sub(r'^🔥\s*', '', title)
    html = f'<div class="feature"><h3>{render_inline(title)}</h3>'

    # 切分段落（空行分隔）
    paragraphs = [p.strip() for p in body.split('\n\n') if p.strip()]
    for p in paragraphs:
        # 跳过分隔线
        if p == '---':
            continue
        # callout：以 **对律所的影响** 或 **为什么重要** 开头
        if re.match(r'^\*\*(对律所|为什么重要|律师视角)', p):
            intro, items = split_callout_circled(p)
            if items:
                html += '<div class="callout">'
                if intro:
                    html += f'<div class="callout-intro">{render_inline(intro)}</div>'
                html += '<ul class="callout-list">'
                for it in items:
                    html += f'<li>{fold_link_clusters(render_inline(it))}</li>'
                html += '</ul></div>'
            else:
                html += '<div class="callout">' + fold_link_clusters(render_inline(p)) + '</div>'
        # 来源行：以 来源： 开头
        elif p.startswith('来源') or p.startswith('中文解读') or p.startswith('⚠️ 一手信源'):
            html += f'<div class="sources">{render_inline(p)}</div>'
        # bullet list（- 开头）
        elif p.startswith('- '):
            items = re.findall(r'^- (.+?)$', p, re.M)
            html += '<ul style="padding-left:24px;font-size:14px;line-height:1.85;color:#3d3832;">'
            for it in items:
                html += f'<li>{fold_link_clusters(render_inline(it))}</li>'
            html += '</ul>'
        # 表格
        elif p.startswith('|'):
            html += render_table(p)
        else:
            html += f'<p>{fold_link_clusters(render_inline(p))}</p>'

    html += '</div>'
    return html


def render_briefs(body: str) -> str:
    """渲染速报区——每条速报作为独立 brief-item。"""
    html = ''
    # 按段落空行切分
    paragraphs = [p.strip() for p in body.split('\n\n') if p.strip() and p.strip() != '---']

    current_item = None
    for p in paragraphs:
        # 一条速报开始：以 **xxx** 开头的段落
        if re.match(r'^\*\*[^*]+\*\*', p) and not p.startswith('**对律所') and not p.startswith('**为什么'):
            if current_item is not None:
                html += current_item + '</div>'
            # 提取标题（**...**）
            m = re.match(r'^\*\*([^*]+)\*\*', p)
            title = m.group(1) if m else ''
            # 剩余文本
            rest = p[len(m.group(0)):].strip() if m else p
            # 把"（日期，来源）："模式拆开
            rest = re.sub(r'^[（(]([^）)]+)[）)]\s*[:：]\s*', '', rest)

            # 拆分描述与 💡 insight 行（速报常用单行 \n 分隔，不会被段落 split 拆开）
            parts = re.split(r'\n\s*-?\s*💡', rest)
            description = parts[0].strip()
            insights = [x.strip() for x in parts[1:]]

            current_item = f'<div class="brief-item"><h4>{render_inline(title)}</h4><p>{fold_link_clusters(render_inline(description))}</p>'
            for ins in insights:
                # 去掉前缀如 "上手："、"关联："
                ins_clean = re.sub(r'^[^：:]{1,8}[：:]\s*', '', ins, count=1)
                current_item += f'<div class="insight">{fold_link_clusters(render_inline(ins_clean))}</div>'
        elif p.startswith('- 💡') or p.startswith('💡'):
            insight = re.sub(r'^- 💡\s*\S*\s*[:：]?\s*', '', p)
            insight = re.sub(r'^💡\s*\S*\s*[:：]?\s*', '', insight)
            if current_item is not None:
                current_item += f'<div class="insight">{render_inline(insight)}</div>'
        elif p.startswith('- '):
            if current_item is not None:
                items = re.findall(r'^- (.+?)$', p, re.M)
                for it in items:
                    if it.startswith('💡'):
                        insight = re.sub(r'^💡\s*\S*\s*[:：]?\s*', '', it)
                        current_item += f'<div class="insight">{render_inline(insight)}</div>'
        else:
            # 其他：附加到当前项
            if current_item is not None:
                current_item += f'<p style="font-size:14px;color:#4a4540;margin-top:6px;">{render_inline(p)}</p>'

    if current_item is not None:
        html += current_item + '</div>'

    return html


def render_table(text: str) -> str:
    """渲染 markdown 表格为 HTML 表格。"""
    lines = [l for l in text.strip().split('\n') if l.strip().startswith('|')]
    if len(lines) < 2:
        return f'<p>{render_inline(text)}</p>'

    # 过滤分隔行 |---|---|
    rows = [l for l in lines if not re.match(r'^\|[\s|:-]+\|$', l)]
    if not rows:
        return ''

    # 解析单元格
    def parse_row(line):
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        return cells

    headers = parse_row(rows[0])
    body_rows = [parse_row(r) for r in rows[1:]]

    html = '<div class="product-table"><table><thead><tr>'
    for h in headers:
        html += f'<th>{render_inline(h)}</th>'
    html += '</tr></thead><tbody>'
    for row in body_rows:
        html += '<tr>'
        for cell in row:
            html += f'<td>{render_inline(cell)}</td>'
        html += '</tr>'
    html += '</tbody></table></div>'
    return html


def render_changes(content: str) -> str:
    """渲染对比表变化点（简单列表）。"""
    html = '<div class="changes">'

    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and p.strip() != '---']
    for p in paragraphs:
        if p.startswith('- ') or p.startswith('* '):
            items = re.findall(r'^[-*] (.+?)$', p, re.M)
            html += '<ul>'
            for it in items:
                html += f'<li>{render_inline(it)}</li>'
            html += '</ul>'
        elif p.startswith('>'):
            quote = re.sub(r'^>\s*', '', p)
            html += f'<p style="font-size:13px;color:#b5ada4;margin-top:12px;">{render_inline(quote)}</p>'
        else:
            html += f'<p>{render_inline(p)}</p>'

    html += '</div>'
    return html


def render_tip(content: str) -> str:
    """渲染本期技巧（自然段落，带步骤列表）。"""
    html = '<div class="tip">'

    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and p.strip() != '---']
    for p in paragraphs:
        if p.startswith('来源') or p.startswith('中文解读'):
            html += f'<div class="sources">{render_inline(p)}</div>'
        elif re.match(r'^\d+\.', p, re.M) or p.count('\n1.') > 0 or p.startswith('1.'):
            # 编号列表
            items = re.findall(r'^\d+\.\s*(.+?)(?=\n\d+\.|\Z)', p, re.M | re.S)
            if items:
                html += '<ol>'
                for it in items:
                    html += f'<li>{render_inline(it.strip())}</li>'
                html += '</ol>'
            else:
                html += f'<p>{render_inline(p)}</p>'
        elif p.startswith('- '):
            items = re.findall(r'^- (.+?)$', p, re.M)
            html += '<ul>'
            for it in items:
                html += f'<li>{render_inline(it)}</li>'
            html += '</ul>'
        else:
            html += f'<p>{render_inline(p)}</p>'

    html += '</div>'
    return html


def render_section(title: str, content: str) -> str:
    """根据板块标题分发到对应渲染函数。"""
    title_clean = re.sub(r'[🔔📡#①②③④⑤\s]+', '', title).strip()

    # 移除 emoji 前缀做匹配
    plain = re.sub(r'[🔔📡①②③④⑤]', '', title).strip()

    is_summary = '今日关键' in plain or '60 秒' in plain or '60秒' in plain
    is_deep = 'AI 深度报道' in plain or '深度报道' in plain
    is_product = '产品速览' in plain
    is_compare = '横向对比' in plain or '对比' in plain
    is_tip = '本期技巧' in plain or '技巧' in plain

    sec_label = ''
    if is_summary:
        sec_label = '60 秒速览'
        body = render_summary(content)
    elif is_deep:
        sec_label = '深度报道'
        body = render_deep_report(content)
    elif is_product:
        sec_label = '产品速览'
        # 找到第一个表格
        m = re.search(r'(\|.+?)(?=\n##|\Z)', content, re.S)
        body = render_table(m.group(1)) if m else f'<p>{render_inline(content)}</p>'
    elif is_compare:
        sec_label = '模型对比动态'
        body = render_changes(content)
    elif is_tip:
        # 技巧标题可能是 "本期技巧：xxx"
        sub = title.split('：', 1)
        sec_label = '本期技巧'
        if len(sub) == 2:
            tip_title = sub[1].strip()
            body = '<div class="tip"><h3>' + render_inline(tip_title) + '</h3>'
            inner = render_tip(content)
            # render_tip 自带 wrapper，去掉
            inner = inner.replace('<div class="tip">', '').replace('</div>', '', 1)
            body += inner + '</div>'
        else:
            body = render_tip(content)
    else:
        sec_label = title
        body = f'<p>{render_inline(content)}</p>'

    return f'<hr class="sep"><div class="sec-title">{sec_label}</div>{body}'


def render_masthead(meta: dict) -> str:
    date = meta.get('date', '')
    info = ' · '.join(filter(None, [meta.get('coverage', ''), meta.get('reading', '')]))
    return f"""<div class="masthead">
  <div class="en">Daily Briefing</div>
  <h1>每日<span class="ai">AI</span>简报</h1>
  <div class="gold-line"></div>
  <div class="meta">
    <span>{date}</span>
    <span>{info}</span>
  </div>
</div>"""


def render_footer(md: str) -> str:
    """提取末尾 *数据来源...*  斜体块作为页脚。

    严格锚定 `*数据来源：` 开头，避免误匹配技巧段中含'数据来源'的 **bold** 文字
    （bug：`**核查每家'训练数据来源'**` 会被旧 regex 错误捕获）。
    """
    matches = re.findall(r'\*(数据来源[:：][^*]+)\*', md)
    if matches:
        # 取最后一个（页脚总在文末）
        return render_inline(matches[-1].replace('|', '<br>').replace('\n', ' '))
    return '本简报由 AI 生成，不构成投资或法律建议'


def convert(md_path: Path, out_path: Path):
    md = md_path.read_text(encoding='utf-8')
    meta = parse_metadata(md)
    sections = split_sections(md)

    masthead = render_masthead(meta)
    body_parts = [render_section(t, c) for t, c in sections]
    body = '\n'.join(body_parts)

    footer = render_footer(md)

    html = HTML_TEMPLATE.format(
        date=meta.get('date', ''),
        css=CSS,
        masthead=masthead,
        body=body,
        footer=footer,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding='utf-8')
    print(f'OK: {md_path.name} -> {out_path}')


def derive_output_path(md_path: Path) -> Path:
    """从 .md 文件名提取日期，输出到 briefings/html/YYYY-MM-DD.html。"""
    name = md_path.stem
    m = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', name)
    if m:
        y, mo, d = m.group(1), m.group(2).zfill(2), m.group(3).zfill(2)
        out_name = f'{y}-{mo}-{d}.html'
    else:
        out_name = name + '.html'
    return md_path.parent / 'html' / out_name


def main():
    if len(sys.argv) < 2:
        print('Usage: python md_to_html.py <briefing.md>')
        sys.exit(1)

    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f'File not found: {md_path}')
        sys.exit(1)

    out_path = derive_output_path(md_path)
    convert(md_path, out_path)


if __name__ == '__main__':
    main()
