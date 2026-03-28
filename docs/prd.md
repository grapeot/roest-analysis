# PRD

## Goal

Provide a reusable Roest analysis toolkit that can fetch roast resources by API, analyze roast logs by log ID, and encode analysis heuristics in a reusable skill.

## Users

- Human operator analyzing roast sessions
- Future agents that need a stable CLI and documented analysis workflow

## MVP scope

- Project scaffold with docs, tests, skill, and local git repo
- Roest API client with known endpoints
- CLI for `doctor config`, `log fetch`, `log analyze`, `machine slots`, and `machine flagged-logs`
- Crack-aware roast analysis with ambiguity handling
- Unit and mocked integration tests

## Non-goals for now

- UI
- Database or long-term storage
- Background sync service
- Full endpoint coverage beyond current known API surface

## Success criteria

- Given a valid log ID, the CLI can fetch the log and datapoints
- The analyzer returns phase metrics and crack candidates
- The analyzer does not blindly trust the first isolated crack point
- The skill documents workflow, pitfalls, and path usage
