# 每日AI晨间简报 - 项目指令

当收到"今日晨报"（或变体：晨报、morning briefing）指令时，按以下流程生成简报。直接执行，无需确认。

---

## 一、时间范围

- 周二至周五：过去24小时
- 周一：过去72小时（涵盖周末）
- 以当前日期和星期判断

## 二、读取近期晨报（去重基线）

在搜索之前，先查找 `briefings/` 目录中的晨报文件，按日期倒序读取：
- **周二至周五：** 读取最近2期
- **周一（72小时版）：** 读取最近3期

读取后记住已报道的主要事件，后续撰写时**全部板块**（①②③④均适用）执行去重：

**基本规则：**
- 近期已报道的事件，若无实质性新进展则不再列入任何板块
- 已深度报道过的事件仅在有重大更新时以速报形式简要跟进（标注"跟进"），不再作为头条
- ④对比表：可直接沿用最近一期的数据，仅标注变化部分

**预告类新闻：** 某产品/大会的预告报道过一次后，正式发布前不得再占头条或要闻——仅在速报中用1-2行提醒时间。正式发布/演讲结束后，以实际内容（而非预告）作为新头条。

**持续性事件（战争、多日会议、多轮融资等）：** 首次报道给全貌（背景+现状），后续各期只写增量变化（新发生了什么），不重复已报道的背景信息。用"第N天""新增"等标记帮助读者快速定位增量。

**判断"实质性新进展"的标准：**
- ✅ 算：正式发布（vs 预告）、新数据/benchmark、人员伤亡/战局重大变化、价格/政策变动、官方确认此前传闻
- ❌ 不算：时间临近（"明天开幕"→"今天开幕"）、媒体评论/分析增多、同一事件换个角度报道

如果找不到历史文件（如首次执行），则跳过此步，正常生成全量内容。

## 三、搜索策略（7-10次，先广后深，新闻+技巧双轨）

**新闻轨（5-8 次，主力）：**

| 轮次 | 搜索内容 | 次数 |
|------|---------|------|
| 广搜 | ① `AI news today {日期}` ② `AI model release update {日期}` | 2次 |
| 中国AI(英) | ③ `China AI news DeepSeek Qwen Doubao {日期}` | 1次 |
| 中国AI(中) | ③b `AI大模型 发布 最新消息 {日期}` | 1次 |
| 国际大事 | ④ `top news today {日期}` | 1次 |
| 定点深挖 | 根据广搜结果，对最重要的1-3个事件追加搜索 | 1-3次 |
| 对比表数据 | ⑤ 搜索最新benchmark/定价信息（如有重大模型发布时） | 0-1次 |

搜索词1-6个词，短小精悍。广搜已覆盖的不重复搜。中文搜索用于捕获国内首发动态。
优先源：TechCrunch、The Verge、Reuters、VentureBeat、arXiv、BBC。

**技巧轨（2-3 次，服务板块 ⑦）：**

| 轮次 | 搜索内容 | 操作 |
|------|---------|------|
| ⑥ GitHub 趋势 | `github trending AI this week` 或直接 WebFetch `https://github.com/trending?since=weekly` | WebSearch / WebFetch |
| ⑦ 工具新特性 | `Claude Code new feature {本月}` / `OpenAI API update {本月}` / `Cursor changelog` | WebSearch + 必要时 WebFetch 官方 changelog |
| ⑧ 法律+AI（机会主义，非每期必做） | 仅当新闻轨涉及法律/合规议题时触发，用法律+AI 专项信源 | WebSearch / WebFetch |

### 实用技巧信源清单（板块 ⑦ 素材库）

**A 类｜一手官方**
- Claude Code 文档 & changelog：https://code.claude.com/docs/
- Anthropic Release Notes：https://docs.claude.com/en/release-notes
- Anthropic 博客：https://www.anthropic.com/news
- OpenAI Cookbook：https://cookbook.openai.com
- Google DeepMind 博客：https://deepmind.google/discover/blog
- Cursor Changelog：https://cursor.com/changelog

**B 类｜GitHub 趋势**
- GitHub Trending（日/周）：https://github.com/trending
- OSS Insight AI 分区：https://ossinsight.io/collections/artificial-intelligence/
- Awesome Claude Code：https://github.com/hesreallyhim/awesome-claude-code

**C 类｜技术博主/社区**
- Simon Willison（英文圈最权威 AI 实战博客）：https://simonwillison.net
- Latent.Space：https://www.latent.space
- r/ClaudeAI：https://reddit.com/r/ClaudeAI
- r/LocalLLaMA：https://reddit.com/r/LocalLLaMA
- Hacker News：https://news.ycombinator.com

**D 类｜AI 工具发现**
- Product Hunt AI：https://www.producthunt.com/topics/artificial-intelligence
- There's An AI For That：https://theresanaiforthat.com

**E 类｜中文社区**
- 少数派 AI 栏目：https://sspai.com/matrix?category=ai
- 知乎 AI 话题：https://www.zhihu.com/topic/ai
- 公众号：机器之心、AI 前哨

**F 类｜法律+AI 专项（用户为律师，机会主义加权）**
- Harvey AI Blog：https://www.harvey.ai/blog
- Damien Charlotin AI 幻觉数据库：https://www.damiencharlotin.com/hallucinations/
- Thomson Reuters Legal AI：https://www.thomsonreuters.com/en/insights/articles/ai-legal-services
- 律新社：https://www.lvxinews.com
- Stanford CodeX：https://law.stanford.edu/codex-the-stanford-center-for-legal-informatics/

### 一手信源 WebFetch 强制规则

搜索只负责"发现新闻"，引用必须 fetch 原文：

- **R3 头条一手信源：** 每条头条（AI 深度报道和国际大事）**必须额外 WebFetch 至少 1 个一手信源**——公司官方 PR/ IR 财报页、官方博客、论文 arXiv 页、法院判决书 PDF、官方社媒原帖等。聚合媒体（CNBC/Reuters/CNN 等）只能作为辅助交叉验证。若一手信源找不到公开 URL，必须在正文说明"未见官方公告"。

- **R5 跟进条目实时数据：** "跟进"类条目中涉及的实时数据（Polymarket 赔率、GitHub commit、官方 changelog、blog 更新、Twitter/X 推文等）**必须 WebFetch 当前实际页面**，不得凭搜索摘要或记忆推测。若 fetch 失败则明确标注"截至 YYYY-MM-DD HH:MM 官方页面未更新"。

## 四、简报结构（5个板块）

### 报头（必须严格遵守此格式）

```
# AI 日报
**YYYY年M月D日 星期X** | 覆盖XX小时 | 预计阅读6-8分钟
```

### ① 今日关键（60 秒速览，3-5 条 bullets）

取代原"今日要闻"执行摘要——改为 bullet 列表便于扫读和转发。**纯 AI / 科技内容，不含国际政治新闻。**

**格式：**
```
🔔 今日关键（60 秒）
- **【事件核心 ≤25 字】**——对律师/法律行业的影响或价值（当相关时，1 句）
- 法律无关条目：省略 dash 后缀，仅写事件核心
```

**示例：**
- **Meta 2026 AI Capex $125B 翻倍**——美股客户估值模型要更新
- **Nebraska 首例律师因 AI 幻觉吊销执照**——AI 写文书必做 citation check

**增量原则：** 近期已报道且无实质性新进展的事件，不再列入。聚焦 24 小时内的增量信息。

### ② AI 深度报道（占 50-60%）

两层结构：头条 + 速报。**纯 AI / 科技内容。**

**时效性规则：** 超过 3 天的事件**不能作为头条**。但可以在速报或实用技巧中作为"实用信息"提及（如"上周发布的 /ultrareview 功能，你可以这样用"）。

**头条（1-2条）：** 发生了什么 + 为什么重要 + 实用信息（能不能用？怎么用？免费/付费？），引用至少2个来源。

**速报（逐条，按重要性排列）：** 每条2-3行，格式统一：
```
**产品名**（日期，来源）：一句话说明
- 💡 上手：一句话最佳用法
```

### ③ AI 产品速览表

```
| 公司 | 产品/更新 | 一句话 | 可用性 | 获取方式 | 日期 |
```

可用性标记必须使用：✅全量 ⏳等待 💰付费 🔧自部署

### ④ 主流AI产品横向对比（沿用机制）

**默认行为：** 读取上期晨报中的 ④ 对比表，**直接沿用**，仅在表后写 1-3 行"📝 本周变化"点评。输出格式：

```
**旗舰/中端对比表与上期一致。** 本周变化：
- 🆕 xxx
- ⏳ xxx
> 完整对比表见 [上期晨报](briefings/晨报_YYYY年MM月DD日.md)
```

**重新生成完整表格的触发条件（仅以下情况）：**
- 新旗舰模型正式发布（如 DeepSeek V4 上线、OpenAI Spud 发布）
- 重大定价变动（>20% 调价）
- 新增对比维度

重新生成时的规则：
- 固定对比：Anthropic旗舰、OpenAI旗舰、Google旗舰（必须纳入）
- 动态对比：选取当期最具竞争力的1-2个其他旗舰模型
- **维度（8 个，律所受众适配）：** 综合推理、办公文档集成、设计/可视化、中文能力、长上下文(实际可用)、定价(input+output/M)、最佳适用、获取方式
- **必须使用⭐星级评分**
- 中端性价比模型同理

### ⑤ 实用技巧（每期必含，条数不设上限）

非新闻性的实用技巧，帮助读者**立刻提升 AI 工具使用能力**。技巧可以独立于当日新闻，来源为"三、搜索策略"技巧轨（搜索 ⑥⑦⑧）+ 实用技巧信源清单（A-F 六类）。当期素材丰富就多写，素材稀薄就精选——不追求数量，追求每条都"读完立刻能用"。

**每条技巧格式：**
```
**技巧名**（类别标签）：一句话摘要
- 🎯 适用场景：什么人、什么时候用
- 🔧 操作步骤：3-5 步 / 一条命令 / 一个配置片段
- ⚠️ 注意：常见坑或限制
- 🔗 来源：[链接]
```

**类别标签（视素材选用）：**
- `Claude Code`、`Prompt 模式`、`工作流`、`GitHub 发现`、`新工具试用`、`踩坑警示`、**`法律+AI`**（机会主义加权，用户为律师）

**选题优先级：**
1. Claude / OpenAI / Google 官方文档刚发布的新特性（Release Notes / Changelog）
2. GitHub 本周 trending AI 项目中的实用小工具（star 数快速增长）
3. 知名实战博主（Simon Willison、Latent.Space）本周新文
4. 主流 AI 工具（Cursor、Perplexity、Claude Code）新发布的 feature
5. **法律+AI 技巧（F 类信源，适度加权）：** 律所受众核心价值——在素材充足时优先选入，不强制每期必出。当期法律议题集中（如监管新规、AI 责任判例）时可写 2-3 条。

**质量红线：**
- ❌ 不得写本项目/本次会话已踩过的坑（避免自我引用失焦）
- ❌ 不得写"如何写好 prompt"这类过于宽泛的建议
- ✅ 必须是"读完立刻能动手"级别的具体——有命令、有路径、有操作步骤
- ✅ 必须附 🔗 来源链接（遵守 R1 禁占位规则）

### 页脚

数据来源 + 免责声明，一行搞定。

## 五、链接要求（必须严格遵守）

1. 所有新闻内容必须附原文链接，格式为 `[来源名](URL)`
2. 原链接必须是官方首发该新闻的链接（如公司官网博客、论文原始页面、官方公告），不得使用其他平台的二手汇总文章
3. 如果原链接域名不是 .cn 或 .com.cn 结尾（即非中国网站），必须额外搜索并附上一个中国媒体对该新闻解读的文章链接，标注为"中文解读"
4. **R1 禁止占位/首页链接：** 找不到真实的中文解读专文时，宁可留空（或标注"暂无中文解读"），不得放 `sohu.com` / `sina.com.cn` / `163.com` 等首页或频道页链接充数。每个链接必须是**具体文章页**，否则视为违规。

## 六、写作规范

- 全文中文，专有名词保留英文
- 语气：专业、简洁、直给
- 每个关键数据标注时间戳（来源+日期）
- 实用性第一：能用就给路径，不能用说清何时能用
- 数据必须来自本次搜索，不凭记忆编造
- 不同来源冲突时标注差异
- 技术细节不回避（参数、benchmark数据等）

### 受众适配（重要）

**用户身份：** 北京汉坤律师事务所律师；晨报会分享给所内同事。所有写作决策以**法律从业者最大价值**为导向。

**处理要点：**
- **优先级加权：** 涉法律/合规/监管/判例的事件（欧盟 AI Act、中国生成式 AI 管理办法、AI 责任判例、GDPR/PIPL、制裁名单、涉外 M&A 管制等）优先纳入，即使当日并非最大新闻
- **法律视角增补：** 非法律主题新闻在"为什么重要"或"上手"段落**主动补一句"对律师/法律行业的影响"**（当相关时）——典型映射：
  - 跨国并购/裁员/融资 → 涉外 M&A 尽调、反垄断申报
  - 金融制裁/出口管制 → 合规业务、出口管制顾问
  - AI 新产品 → 律师使用场景、合规审查义务、知识产权影响
  - 地缘政治 → 跨境业务风险、客户咨询热点
- **技术细节节制：** 模型架构、训练方法、激活参数等纯技术内容**简化或省略**，让位给影响面和实用性
- **法律+AI 显性加权：** 板块 ⑤ 实用技巧中，法律+AI 类技巧在素材充足时优先选入（非强制每期必含，见 §四.⑤）

### R6 技术指标人话脚注

所有 benchmark 分数和技术术语在**当期首次出现时**必须括号内补充人话解释：

- ✅ 合格：`GPQA 94.3%（研究生级科学推理测试，顶级博士约 65%）`
- ✅ 合格：`SWE-bench 78.8%（真实软件工程任务实测通过率）`
- ✅ 合格：`OSWorld 75%（操作系统 Agent 任务，人类基线约 72%）`
- ✅ 合格：`Mythos 级（Anthropic ASL-4 安全协议分级，最高级）`
- ❌ 不合格：单独写 `GPQA 94.3%` 或 `SWE-bench 78.8%` 不加解释

同一期后续再提及同一指标可省略脚注。若无法找到可靠人话解释则**整个删除该指标**而非硬塞——宁可不写，不写错。

**数据时间戳格式：**
- 产品发布/更新 → "2月17日发布"
- 融资/并购 → "2月14日公告"
- 研究论文 → "2月10日 arXiv"
- 市场数据 → "2月22日 Motley Fool数据"
- 信息不确切时 → "据报道" + 来源说明

**R2 数据口径一致性（对比表强制）：** 所有跨公司/跨产品对比表，同一列必须使用同一口径。典型如 Capex 表：全部用"年度"或全部用"单季度"，不得混用；不得不混用时必须在列头注明（例如"Microsoft 数据为 FY26 Q2 单季度，其他为 2026 全年指引"）。benchmark、定价、参数量等同样要求口径一致。

**R4 分析师预测强制归因：** 所有第三方预测/估算必须归因到**机构名 + 报告日期 + 分析师姓名（若可查）**。
- ✅ 合格：`Barclays 分析师 Ross Sandler 在 4 月 8 日报告中预测 Meta 自由现金流 2026 年下降 90%`
- ❌ 不合格：`Barclays 分析师警告 FCF 下降 90%`、`分析师预计 Amazon 自由现金流转负`
- 若仅查到机构名、找不到具体分析师+日期，必须显式说明"来源：XX（分析师姓名/日期未披露）"，提醒读者验证成本

## 七、完成后执行步骤

1. 将晨报保存到 `briefings/晨报_YYYY年MM月DD日.md`
2. 执行 `git add briefings/ && git commit -m "晨报 YYYY-MM-DD" && git push`，触发 GitHub Actions 自动邮件发送
3. 输出 **3-5 句中文核心看点总结**
4. 输出 **邮件主题行**，格式为：`晨报 M/D｜最重要事件短语一·短语二·短语三`（用 · 分隔，总长控制在 60 字以内，便于邮件客户端完整显示）
   - 示例：`晨报 4/22｜Trump 延长伊朗停火·Meta 豪掷$125B·Nebraska 律师因 AI 幻觉吊销`
