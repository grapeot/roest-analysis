# AGENTS.md

## Project purpose

This project is a reusable Roest API and roast analysis toolkit. Keep it as a maintainable Python project, not a pile of one-off scripts.

## Structure

- `docs/` holds project intent, design, test strategy, and work log
- `skills/roest_analysis.md` is the canonical project-local skill
- `src/roest_analysis/` holds reusable library code
- `scripts/roest` is the stable shell entrypoint
- `tests/` contains unit and integration coverage

## Working rules

- Update `docs/working.md` after meaningful changes
- Keep API transport separate from roast analysis heuristics
- Keep crack analysis sequence-aware and cluster-aware
- Do not print or log the raw API token
- Prefer the workspace `.venv` unless isolation is required later

## Validation

- Run `python -m pytest -v`
- Run `python -m roest_analysis.cli doctor config`
- Run at least one `log analyze` smoke command when API access is configured
