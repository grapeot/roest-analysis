# PRD

## 产品定位

`roest_analysis` 是 AI-first 咖啡烘焙闭环的基础设施层。

这个项目的出发点是一个观察：咖啡烘焙正在经历一次问题空间的根本迁移，而 AI 恰好处在这次迁移的最佳介入位置。

传统模式下，烘焙者的核心工作是两件事：perception（听声、看色、闻味）和 control（调火力、调风门、决定下豆时机）。两者都高度依赖感官和肌肉记忆，知识以个人经验的形式存在，难以外化、难以传递、难以规模化。新一代可编程烘焙机通过传感器阵列、PID 温控和可编程 profile 把 perception 和 control 都交给了硬件，人的精力从执行层转向了策略层——理解烘焙原理、分析风味表现、设计和迭代 profile。

这个迁移同时创造了一个新的机会和一个新的瓶颈。机会在于：传感器产生了大量结构化数据，而 Roest 的 API 直接以 JSON 形式输出。AI agent 可以自主拉取、分析、可视化、生成诊断报告，无需人在中间做格式转换或口头描述。瓶颈在于：如果没有可靠的数据通路和编码好的分析规则，这些数据仍然是沉睡的。这个项目就是要把数据通路打通，让 AI 成为烘焙流程的 first-class 参与者。

长期方向是把烘豆从依赖个人技艺的手工模式，推向可复制、可迭代、可产品化的系统模式。价值增长的主要路径是 domain knowledge 注入——烘焙原理、豆种特性、风味化学编码成 skill 和 knowledge base，让 AI 获得领域深度。这条路径的核心前提是可靠的数据获取和一致的分析口径，就是这个项目提供的东西。

## 用户画像

### 1. AI agent（第一优先级）

AI 是这个项目的核心用户。它需要：稳定的 CLI 接口、确定性的输出格式、编码好的分析规则。AI 不需要猜测字段含义，不需要从自然语言描述中还原数据，它直接从 API 获取结构化数据，通过 CLI 调用分析逻辑，产出可解释的诊断结果。

在闭环中 AI agent 的角色不限于被动分析。随着 knowledge base 的积累，它可以主动推荐 profile 调整、跨批次识别趋势、标记异常模式。这些能力的基础是可靠的数据获取和一致的分析口径。

### 2. 人类烘焙者

想快速回答：这一锅到底哪里出了问题、最近几锅有没有变好、一爆前后是冲太快还是掉太狠、哪个 crack 点是真正该拿来算 development 的。人类用同一套 CLI 和图表，和 AI 使用完全相同的分析口径。

### 3. 项目维护者

希望这个仓库可以公开到 GitHub，而不暴露 credential、machine 信息或本地路径依赖。

## 产品思想

### 闭环，而非工具

这个项目的设计目标不是做一个好用的 CLI 工具然后停在那里。它是闭环中的一个关键组件：数据采集 → 分析诊断 → 知识积累 → 策略调整 → 下一次烘焙。闭环的意义在于每一次烘焙的结果都能系统性地回馈到下一次决策中，而 AI 可以自主驱动从数据到洞察的全过程，人的参与集中在策略决策和知识补充上。

过去的烘焙优化是线性的：烘一锅，喝一杯，凭记忆调整下一锅。闭环模式下，每次烘焙的完整数据都被保留、分析、对比，趋势和模式可以被识别，调整建议可以被量化。这才是从个人技艺走向系统化的关键路径。

### 分析规则即 domain knowledge

crack 不能只看第一个点、practical onset 和 active cluster 要区分、两阶段 crack 要保守解释 development——这些规则就是 domain knowledge 的编码形式。它们是产品的核心资产，而非工程实现细节。随着烘焙经验的积累，这些规则会持续演进，这正是 knowledge base 驱动价值增长的具体体现。

### AI 和人共享同一套真相

同一条命令、同一套分析逻辑、同一张图表。人看到的和 AI 看到的完全一致。这消除了传统模式中人工描述到 AI 理解之间的信息损失，也保证了诊断结论的可复现性。

### 问题边界

这个项目解决的是从原始传感器数据到结构化诊断洞察这一段。它不解决风味判断（杯测仍然是人的领地），不解决 profile 自动生成（这需要更多积累），不解决硬件控制（那是烘焙机固件的事）。清晰的边界意味着这个组件可以被其他系统可靠地依赖。

## 当前范围（Phase 2）

- 保留现有 API client、分析逻辑和测试体系
- `log plot` visualization 能力
- 可嵌入 README 的示例图
- 两阶段 crack 的保守解释
- 中文文档体系（README 双语、PRD、RFC、CLAUDE.md）
- public repo 前的 security review

## 关键能力

### 1. Roast 获取

按 log ID 抓取 log detail 和 datapoints，按 machine 列出 logs，查询 machine slots 和 flagged logs。

### 2. Roast 分析

计算 turning point、yellow、practical onset、development。区分 practical crack onset 和 active crack cluster。对 crack outlier 和 split cluster 给出明确 note。

### 3. Roast 可视化

一张图展示 bean temperature、inlet temperature、ROR30、heat/fan 控制量、crack signal 与 onset 标记。matplotlib 渲染 SVG，GitHub 可直接显示。

### 4. AI-first 工作流

CLI 适合 agent 直接调用。skill 文档记录分析规则和常见坑。CLAUDE.md 告诉 AI 在这个仓库里怎么安全地参与闭环。

## 非目标

- Web UI
- 数据库存储
- 后台同步服务
- 完整覆盖 Roest 所有 API
- 杯测结论自动化替代人的判断（杯测仍然是人的领地，AI 做的是数据侧的诊断）
- Profile 自动生成（需要更多 domain knowledge 积累后再考虑）

## 成功标准

- 给定 `<log-id>`，CLI 能 fetch、analyze、plot
- analyzer 不会把第一个孤立 `crack` 点当成 ground truth
- 对两阶段 crack 会给出保守解释，而不是单点定论
- README 能让新用户通过两个案例理解系统价值和分析口径
- AI agent 可以无人工介入地完成从数据拉取到诊断输出的完整流程
- 默认测试和显式 live integration 测试都可运行
- 仓库达到可公开但未 push 的状态
