# 测试策略

## 目标

这个项目的测试不是只验证“代码能跑”，而是验证三件事：

1. API 抓取链路可靠
2. roast 分析口径稳定，尤其是 crack 解释不能退化
3. CLI 和文档里承诺的工作流对人类和 AI 都真实可用

## 单元测试

单元测试覆盖这些核心逻辑：

- `.env` 配置解析
- crack clustering、outlier 过滤和 onset 选择
- phase metrics 计算
- practical onset / active onset 双层 development 解释
- visualization 所需的序列提取

这部分应当保持纯逻辑、低耦合，不依赖真实 API。

## 集成测试

集成测试分两层：

### 1. Mocked integration

通过 mocked transport 或假 client 验证：

- API client 的 endpoint 拼装是否正确
- CLI 输出 contract 是否稳定
- `log plot` 是否能产出 SVG 文件
- machine 相关命令是否能从环境变量回退读取 `ROEST_MACHINE_ID`

### 2. Live integration

真实 API 集成测试用于验证完整链路：

- 能列出 machine logs
- 能抓取至少一个真实 log 与 datapoints
- 能对真实 roast 跑完整分析

## Live integration 规则

- 默认必须 skip
- 只有在 `.env` 配好真实 credential 时才有意义
- 只有在显式设置 `ROEST_ENABLE_LIVE_TESTS=1` 时才运行
- machine id 来自 `.env` 的 `ROEST_MACHINE_ID`，不要在代码里写死

运行方式：

```bash
python -m pytest -v
ROEST_ENABLE_LIVE_TESTS=1 python -m pytest -v -m live_integration
```

## 手工 smoke checks

每次重要改动后，至少做这些检查：

- `python -m roest_analysis.cli doctor config`
- `python -m roest_analysis.cli machine logs`
- `python -m roest_analysis.cli log analyze --log-id <log-id>`
- `python -m roest_analysis.cli log plot --log-id <log-id> --output docs/assets/example.svg`

如果本地没有 `.env` 或者不想命中真实 API，就只跑默认测试，不跑 live integration。

## 发布前检查

在准备公开到 GitHub 之前，测试之外还要补做这几项核验：

- `.env` 没有被 git 跟踪
- `.env.example` 只保留占位符
- 文档、fixture、示例图命名里没有真实 machine id 或本地路径
- `doctor config` 只输出 masked token
