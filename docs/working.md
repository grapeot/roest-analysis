# 工作记录

## 变更日志

### 2026-03-27 — 文档升级：AI-first 闭环 framing 与双语化

核心变化是把项目定位从"Roest API 分析工具"升级到"AI-first 咖啡烘焙闭环"。这个 framing 变化反映的是一个实际观察：新一代烘焙机通过传感器和可编程 profile 把 perception + control 交给了硬件，AI 通过结构化 API 直接消费数据，整个闭环可以在 AI 主导下运转，人的精力集中在策略和风味判断上。这个 repo 用 API 打通、分析规则编码、可视化落地和 live tests 证明这条路径可行。

具体改动：

- **README.md**：改为双语单文件结构，中文主文档在前、英文完整版在后，顶部有跳转链接。开篇从问题背景（感官依赖 → 硬件解放 → API 消除翻译层 → AI first-class citizen）完整铺开。案例保留 round 1 和 round 3 两个，不再写 round 4。对两个案例的说明文字补充了更多分析口径的描述
- **docs/prd.md**：补充了产品思想层面的内容——闭环 vs 工具的区别、分析规则即 domain knowledge、AI 和人共享同一套真相、问题边界的定义。用户画像和成功标准与新 framing 对齐
- **docs/rfc.md**：在每个设计决策后补充了它对闭环系统的意义。双层 crack 口径的解释补充了声学信号流的背景。sanitize 策略补充了原则性描述。CLI 合同补充了 AI 和人共享入口的设计意图。deferred 部分增加了跨批次趋势分析
- **CLAUDE.md**：从"操作手册"升级到"闭环参与指南"。告诉 AI 如何读取上下文、如何基于 CLI/JSON/可视化推进分析与迭代、如何在数据诊断和风味判断之间划界、如何持续保持 sanitize
- **docs/working.md**：记录本轮变更

未改动代码逻辑、测试策略文档 (docs/test.md)、或其他文件。

### 2026-03-27

- 初始化 `adhoc_jobs/roest_analysis` 项目骨架，补齐 docs、tests、skill、脚本入口和独立 git repo
- 实现 Roest API client、CLI、roast analysis 模块，以及基于 `.env` 的本地配置加载
- 建立单元测试、mocked integration tests 和默认 skip 的 live integration tests
- 增加 machine logs 查询能力，让真实集成测试可以先列 roast，再挑样本做分析
- 修正 `.env` 根路径解析、测试导入路径和 `src/` layout 的静态分析配置
- 强化 crack 解释规则：不再把第一个孤立 `crack` 点直接视为 first crack，而是基于完整序列和 cluster 做判断
- 增加 practical onset / active onset 双层口径，并在两阶段 crack 时提示保守解释 development
- 实现 `log plot`，输出可直接嵌入文档的 SVG 图表，覆盖 bean temp、inlet temp、ROR30、heat、fan 和 crack signal
- 生成公开示例图，并最终保留 round 1 与 round 3 两个完整 roast 作为 README 示例
- 将 machine 配置迁移到 `.env`，同时对 README、tests、fixtures 和示例命名做 sanitize，避免公开仓库泄露真实环境信息
- 重写 README、PRD、RFC、CLAUDE.md 等文档，使项目更适合以 GitHub public repo 的方式发布
- 完成默认测试、live integration tests、CLI smoke checks 和基础 security review
- 将 roast visualization 从手写 SVG 渲染切换为 matplotlib，解决纵轴无数字和 crack signal 面板易被截断的问题，并重新生成公开示例图

## 当前状态

- 核心 fetch / analyze / plot 工作流已经可用
- 默认测试通过，真实 API 集成测试在显式启用时通过
- 示例图、技能文档和 AI 使用说明已经接通
- 文档已完成 AI-first 闭环 framing 升级和双语化
- 仓库尚未 push，仍处于可公开待最终确认的状态

## 经验与结论

- Roest 的 `crack` 更适合被理解为声学检测流，而不是绝对可靠的单点事件
- practical onset 和 active onset 需要同时保留，尤其是在 split-cluster crack 场景里
- live integration tests 必须默认 skip，只有在显式配置 `.env` 且用户要求时才运行
- 公共文档里不要硬编码 machine id、log id 或本地路径
- README 里的示例应该优先展示完整 roast；未完成 roast 可以用于调试，但不适合作为主案例
- 项目 framing 从"分析工具"到"AI-first 闭环"的升级需要落到具体能力上（API 打通、规则编码、可视化、live tests），空喊口号没有说服力
