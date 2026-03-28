# CLAUDE.md

## 这个仓库是做什么的

AI-first 咖啡烘焙闭环项目。Roest 烘焙机的 API 输出结构化 JSON（时间序列温度、ROR、控制量、crack 检测信号），你可以自主拉取数据、写分析程序、生成可视化、形成假设、修正判断。

闭环路径：数据采集 → 分析诊断 → 知识积累 → 策略调整 → 下一次烘焙。你负责前三段，人负责策略决策和风味判断。

## 工作环境

CLI 是你和人类共享的数据入口，保证分析口径一致。常用命令：

```bash
python -m roest_analysis.cli doctor config
python -m roest_analysis.cli machine logs --machine-id "$ROEST_MACHINE_ID"
python -m roest_analysis.cli log analyze --log-id <log-id>
python -m roest_analysis.cli log plot --log-id <log-id> --output docs/assets/example.svg
```

原始 JSON 数据可以通过 `log fetch --resource bundle --format json` 获取。如果内置分析不够用——比如你需要做跨批次统计、趋势拟合、自定义可视化——直接对 JSON 数据写代码。CLI 是起点，不是天花板。

文档在你需要时去读。`docs/working.md` 记录了最近发生的事，`docs/prd.md` 描述了产品定位和边界，`skills/roest_analysis.md` 记录了分析规则和常见坑。

## 你的角色

你在这里是诊断者和研究者，不是报告模板的填充器。面对一组 roast 数据时，你应该形成自己的判断：哪些指标异常，异常的可能原因是什么，和相邻批次对比后趋势如何，是否需要更多数据才能得出结论。

当你有足够数据支撑某个观察时，可以主动提出 profile 调整建议、跨批次趋势总结、或分析规则本身需要更新的地方。但要区分数据侧诊断和风味侧判断——杯测结论是人的领地。

## 分析原则

Roest 的 crack 传感器输出的是声学信号流，早期孤立点可能是噪声。看完整 crack 序列和 cluster，区分 `practical_onset` 和 `active_onset`。当两者分离明显时，对 development 的解释要保守。incomplete log 只能做过程判断，给不了完整 roast 结论。

## 安全

这个仓库计划公开到 GitHub，sanitize 是持续性要求。`.env` 是本地文件，不加入 git。公开材料里用 `<log-id>` 和 `$ROEST_MACHINE_ID` 占位，不写死真实凭据。每次修改文档或测试后，留意是否意外引入了真实环境信息。

## 测试

默认 `python -m pytest -v` 跑 unit tests 和 mocked integration tests。真实 API 测试需要 `.env` 配好并显式启用：`ROEST_ENABLE_LIVE_TESTS=1 python -m pytest -v -m live_integration`。修改分析逻辑后跑一遍默认测试。

## 文档维护

重要改动记录到 `docs/working.md`。README 面向人类读者，双语结构（中文在前、英文在后）。`skills/roest_analysis.md` 面向 AI 工作流，强调分析原则和边界。PRD 和 RFC 体现产品思想和系统边界。
