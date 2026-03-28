# CLAUDE.md

## 这个仓库是做什么的

这是一个面向 Roest roast log 的 AI-first 分析项目。目标不是只把 API 数据抓下来，而是把 roast diagnostics 里的判断规则固化成可重复调用的工具。

## 你应该怎么使用它

优先走 CLI，而不是自己手搓 HTTP 请求。

常用命令：

```bash
python -m roest_analysis.cli doctor config
python -m roest_analysis.cli machine logs --machine-id "$ROEST_MACHINE_ID"
python -m roest_analysis.cli log analyze --log-id <log-id>
python -m roest_analysis.cli log plot --log-id <log-id> --output docs/assets/example.svg
```

## 分析 roast 时的硬规则

1. 不要把第一个 `crack` 点直接当作 first crack
2. 一定要看完整 crack 序列和 cluster
3. 如果 `practical_onset` 和 `active_onset` 分离明显，要保守解释 development
4. incomplete log 只能做过程判断，不能给完整 roast 结论

## 安全规则

1. `.env` 是本地文件，不要加入 git
2. 不要在输出、文档、测试 fixture 里打印原始 token
3. 公开材料里不要写死真实 machine id 和 log id
4. `.env.example` 只能放占位符

## 测试规则

- 默认运行：`python -m pytest -v`
- 真实 API 测试：`ROEST_ENABLE_LIVE_TESTS=1 python -m pytest -v -m live_integration`
- live tests 默认应该 skip，只有显式启用时才运行

## 文档维护

- 每次有重要改动都更新 `docs/working.md`
- README 面向人类读者，强调直觉、价值和例子
- `skills/roest_analysis.md` 面向 AI 工作流，强调规则和坑
