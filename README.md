# 每日AI晨报 - 自动邮件发送

**架构：** Cowork 生成晨报（免费，用订阅账户）→ git push 到 GitHub → GitHub Actions 自动发邮件

## 工作流程

```
每天10:00 (北京时间)
  ↓
Cowork 定时任务启动
  ↓
Claude 搜索 + 生成晨报 (用你的订阅，$0)
  ↓
保存 晨报_YYYY年MM月DD日.md
  ↓
git push 到 GitHub
  ↓
GitHub Actions 自动触发
  ↓
读取 .md → 转 HTML → SMTP 发邮件
  ↓
qihanwei97@gmail.com
846522714@qq.com
hanwei.qi@hankunlaw.com
yaohuanjia1997@163.com
```

## 部署步骤

### 第1步：创建 GitHub 仓库 + 推送代码

```bash
cd "D:\OneDrive - 北京市汉坤律师事务所\思考\daily-briefing"
git init
mkdir briefings
echo "placeholder" > briefings/.gitkeep
git add .
git commit -m "init: daily briefing email automation"
git remote add origin https://github.com/你的用户名/daily-briefing.git
git branch -M main
git push -u origin main
```

### 第2步：配置 Gmail App Password

1. 打开 https://myaccount.google.com/apppasswords
2. 选择「邮件」→「其他」→ 输入名称 `daily-briefing`
3. 复制生成的16位密码

### 第3步：配置 GitHub Secrets

进入仓库 → Settings → Secrets and variables → Actions → New repository secret

| Secret 名称 | 值 |
|---|---|
| `SENDER_EMAIL` | `qihanwei97@gmail.com` |
| `SMTP_PASSWORD` | 第2步的16位密码 |
| `SMTP_HOST` | `smtp.gmail.com` |
| `SMTP_PORT` | `587` |
| `RECIPIENTS` | `qihanwei97@gmail.com,846522714@qq.com,hanwei.qi@hankunlaw.com,yaohuanjia1997@163.com` |

### 第4步：配置 Git 凭证（让 Cowork 能 push）

在你的电脑上运行：
```bash
git config --global credential.helper store
```

然后手动 push 一次（输入 GitHub 用户名和 Personal Access Token），凭证会被保存。

生成 Personal Access Token：
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 勾选 `repo` 权限
3. 生成并保存 token（作为密码使用）

### 第5步：测试

手动 push 一个晨报文件测试：
```bash
cd "D:\OneDrive - 北京市汉坤律师事务所\思考\daily-briefing"
copy ..\晨报_2026年02月28日.md briefings\
git add briefings/
git commit -m "test: briefing email"
git push
```

然后去 GitHub Actions 页面查看是否触发，检查邮箱是否收到。

### 完成！

之后每天10点：
1. ✅ Cowork 自动生成晨报（$0，用订阅）
2. ✅ 自动 push 到 GitHub
3. ✅ GitHub Actions 自动发邮件到4个邮箱

## 费用

| 项目 | 费用 |
|------|------|
| Cowork 生成晨报 | $0（含在 Claude 订阅中） |
| GitHub Actions | $0（私有仓库免费额度 2000分钟/月，每次约1分钟） |
| Gmail SMTP | $0 |
| **总计** | **$0/月** |

## 修改收件人

更新 GitHub Secrets 中的 `RECIPIENTS`，多个邮箱用英文逗号分隔。

## 文件结构

```
daily-briefing/
├── .github/workflows/
│   └── daily-briefing.yml    # GitHub Actions 配置
├── briefings/                 # 晨报文件存放目录
│   └── 晨报_2026年02月28日.md
├── send_email.py              # 邮件发送脚本
├── requirements.txt
└── README.md
```
