# RFC

## 架构总览

项目保持四层结构，Phase 2 补了 visualization 层：

1. `config.py`：读取 `.env`，管理 token、timeout、machine_id 等运行参数
2. `api/`：Roest HTTP 请求与 endpoint 封装
3. `analysis/`：phase metrics、crack clustering、summary 等纯分析逻辑
4. `visualization/`：把 datapoints 规范化成可绘图序列，再用 matplotlib 渲染成 SVG
5. `services/` + `cli.py`：面向用户和 AI 的稳定入口

这个分层服务于 AI-first 闭环的核心需求：AI agent 通过 CLI 层调用分析和可视化，获得与人类完全一致的诊断结果。分层的意义在于每一层都可以被独立测试、独立演进，同时保证 AI 和人看到的输出严格一致。

## 设计决策

### 1. 可视化选型：matplotlib

可视化最初用标准库手写 SVG，后切换到 matplotlib。手写 SVG 在纵轴标注、多面板布局和 crack signal 面板的空间分配上遇到了工程阻力，matplotlib 用更少的代码解决了这些问题。当前唯一的外部依赖就是 matplotlib（`pyproject.toml` 中声明），输出仍然是 SVG 格式，GitHub 可直接渲染。

这个选择是实用权衡：matplotlib 是 Python 生态中最广泛安装的绘图库，AI agent 在自动化流程中使用它几乎不会遇到环境问题。

### 2. 分析逻辑与可视化分离

`visualization/series.py` 只负责把 datapoints 归一化成：

- `time_s`
- `bean_temp`
- `inlet_temp`
- `ror30`
- `heat`
- `fan`
- `crack_points`

这样 visualization 可以重用分析结果，但不会把图表渲染逻辑反向耦合进 core analysis。这个分离对闭环系统很重要：分析规则是 domain knowledge 的编码，它的演进节奏应该独立于展示层。

### 3. crack 解释采用双层口径

系统同时追踪：

- `practical_onset`：第一个有意义的 crack cluster
- `active_onset`：真正变得明显、持续、强度更高的 cluster

如果这两者明显分离，就把结果标成更高歧义，并要求保守解释 development。

这个设计来自实际烘焙数据的观察：Roest 的 crack 传感器检测的是声学信号流，而非绝对可靠的单点事件。早期孤立的 crack 信号可能是噪声或者预兆性的微裂，和真正的一爆主体有本质区别。双层口径让系统在面对这种歧义时给出诚实的判断，而非制造虚假精度。

### 4. 对 incomplete log 也要可视化

最新 roast 未必已经 drop。可视化不能只支持完整 roast，也要能对早期数据画图，这样用户才能在 roast 还没结束时判断当前走向。这对闭环的实时性有直接价值。

### 5. public repo sanitize 策略

为了方便公开到 GitHub：

- machine id 不写死在代码和文档里，放进 `.env`
- `.env.example` 只保留占位符
- README 和示例图不用真实 log id 当标题或文件名
- live tests 使用环境配置和动态列 log，而不是硬编码真实 ID

sanitize 的原则是：公开仓库里的任何内容都不应该能被用来直接访问真实设备或数据。

## CLI 合同

当前面向用户的主要命令：

- `doctor config`
- `log fetch`
- `log analyze`
- `log plot`
- `machine logs`
- `machine slots`
- `machine flagged-logs`

其中 `log plot` 的 contract 是：

```bash
python -m roest_analysis.cli log plot --log-id <log-id> --output docs/assets/roast.svg
```

CLI 是 AI agent 和人类共享的唯一入口。所有诊断能力都通过 CLI 暴露，不存在只有人能用或只有 AI 能用的路径。这个设计选择保证了分析口径的一致性。

## 图表结构

每张图分四个 panel（matplotlib 渲染为 SVG）：

1. Temperature
2. ROR30
3. Controls
4. Crack signal

并叠加两条垂直标线：

- `practical_onset`
- `active_onset`

这样一张图就能同时回答：

- 温度推进是否合理
- 一爆前后 ROR 在怎么变化
- fan / heat 有没有制动
- crack 是不是分成两个阶段

## 缺失字段处理

如果 datapoints 没有 `inlet_temp`，系统会：

- 回退到 `tc1`
- 如果仍然没有，就在图里省略 inlet 线
- 并在 notes 里明确写出这个限制

## 后续仍然保留为 deferred 的部分

- 批量生成多个 roast 的对比图
- 更细的 annotation 与 cup notes 模板
- CSV / parquet 导出
- 更成熟的 ambiguity ranking 策略
- 跨批次趋势分析（闭环的下一步自然延伸）
