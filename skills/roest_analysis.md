# Roest Analysis Skill

## 这是什么

一个面向 AI 的咖啡烘焙诊断环境。你可以通过 CLI 直接访问 Roest API，拉取结构化时间序列数据，做 phase 分析，生成可视化，并对烘焙行为形成假设。目标是基于数据的诊断推理，而非机械的报告生成。

## 文件位置

项目本地的源文件：`adhoc_jobs/roest_analysis/skills/roest_analysis.md`。全局入口：`rules/skills/roest_analysis.md`。项目目录：`adhoc_jobs/roest_analysis/`。

## 环境和工具

Token 和 machine ID 从项目根目录的 `.env` 加载。CLI 是 AI 和人共享的数据入口，常用命令：

```bash
python -m roest_analysis.cli doctor config
python -m roest_analysis.cli log fetch --log-id <log-id> --resource bundle --format json
python -m roest_analysis.cli log analyze --log-id <log-id> --format text
python -m roest_analysis.cli log plot --log-id <log-id> --output docs/assets/example.svg
python -m roest_analysis.cli machine logs --machine-id "$ROEST_MACHINE_ID"
python -m roest_analysis.cli machine slots --machine-id "$ROEST_MACHINE_ID"
python -m roest_analysis.cli machine flagged-logs --machine-id "$ROEST_MACHINE_ID" --event-flags 36
```

CLI 是起点，不是天花板。如果需要做跨批次统计、趋势拟合、异常检测这类内置命令覆盖不到的分析，直接对原始 JSON 数据写代码。

## 分析原则

**Crack 解释是最难的部分。** Roest 的 crack 传感器输出的是声学检测流，不是可靠的单点事件标记。第一个非零 crack 数据点经常是噪声或前驱爆裂，不是真正的一爆起始。系统追踪两个口径：`practical_onset`（第一个有意义的 cluster）和 `active_onset`（持续的高强度 cluster）。当两者分离明显时，development 计算会变得模糊，系统会显式标注这一点，而非选一个值假装精确。

**模糊性本身是信息，不是失败。** 如果 crack cluster 强度相近，如果 practical 和 active onset 分离显著，如果 log 不完整——直说。一个带有明确不确定性的保守解释，比一个自信但错误的结论有用得多。

**单次烘焙分析有天然局限。** 一次烘焙告诉你这一锅发生了什么。模式和趋势只有在多次相似 profile 的对比中才能浮现。在判断某个 profile 调整是否有效之前，先看相邻的实验批次。

**控制动作和热响应是耦合的。** ROR 异常（尖峰、塌陷、平台）几乎总能对应到一个控制动作。诊断 ROR 问题时，检查前 30-60 秒的 heat 和 fan 变化。

## 边界

这个 skill 覆盖的是从原始传感器数据到结构化诊断洞察的路径。它不涵盖风味判断（杯测是人的领地）、profile 自动生成（需要更多积累的领域知识）、或硬件控制（那是烘焙机固件的事）。保持这些边界清晰，意味着诊断输出可以被其他系统或人类决策可靠地消费。

## 常见坑

把第一个非零 `crack` 数据点当作一爆。把 API 得到的 crack 时间点等同于人耳听到的。只看一次烘焙就下宏观结论。忽略 crack 前后的 heat/fan 控制变化。在公开输出中打印或硬编码真实的 bearer token、machine ID 或 log ID。

## 安全

Token 和 machine ID 存放在 `.env`（已 gitignore）。公开材料使用 `<log-id>` 和 `$ROEST_MACHINE_ID` 作为占位符。任何输出、文档或测试 fixture 中都不能暴露真实凭据。
