# roest_analysis

Roest roast log retrieval and analysis toolkit.

## What it does

- Fetches Roest resources with a project-local bearer token from `.env`
- Retrieves roast logs and datapoints by log ID
- Analyzes roast datapoints with crack-aware heuristics
- Exposes a CLI for config checks, fetch, and analysis

## Quick start

```bash
source /Users/grapeot/co/knowledge_working/.venv/bin/activate
python -m pytest -v
python -m roest_analysis.cli doctor config
python -m roest_analysis.cli log analyze --log-id 3598319
```

## CLI examples

```bash
python -m roest_analysis.cli log fetch --log-id 3598310 --resource datapoints --format json
python -m roest_analysis.cli log fetch --log-id 3598310 --resource log --format json
python -m roest_analysis.cli log analyze --log-id 3598319 --format text
python -m roest_analysis.cli machine logs --machine-id 2559
python -m roest_analysis.cli machine slots --machine-id 2559
python -m roest_analysis.cli machine flagged-logs --machine-id 2559 --event-flags 36
```

## Notes

- `.env` is gitignored on purpose.
- Crack inference is sequence-aware. Do not trust the first isolated `crack` point.
- The canonical skill lives in `skills/roest_analysis.md`.
