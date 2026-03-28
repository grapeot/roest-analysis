# Test Strategy

## Unit

- config parsing
- crack clustering and onset selection
- phase metrics
- text summary generation

## Integration

- API client request formatting with mocked transport
- CLI command behavior and output contracts
- service orchestration with fixtures

## Live integration

- gated by `ROEST_ENABLE_LIVE_TESTS=1`
- requires a valid `.env`
- verifies at least one log fetch and analyze path end to end

## Manual smoke checks

- `python -m roest_analysis.cli doctor config`
- `python -m roest_analysis.cli log analyze --log-id <id>`
