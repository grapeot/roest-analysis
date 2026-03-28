# Working

## Changelog

### 2026-03-27

- Scaffolded the `adhoc_jobs/roest_analysis` project with docs, tests, skill folder, and local git repo
- Implemented a standard-library Roest API client, CLI commands, and crack-aware roast analysis modules
- Added mocked integration tests and env-gated live integration tests, including listing logs and analyzing the first three live logs
- Added a machine log listing command so live tests can fetch candidate logs before analysis
- Fixed project root resolution for `.env`, added test import path support, and aligned static typing with the package layout
- Removed an unnecessary package import cycle and added explicit static-analysis config for the `src/` layout

## Lessons Learned

- Roest `crack` detections should be treated as a sequence signal, not a single-event ground truth
- Project-local skill content is the canonical source; global skills should point to it clearly
- Live integration tests should stay skipped by default and only run when explicitly enabled through env
