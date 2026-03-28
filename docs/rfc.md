# RFC

## Architecture

The project is split into four layers:

1. `config.py`: load `.env`, validate runtime configuration
2. `api/`: raw transport and endpoint wrappers
3. `analysis/`: pure roast analysis logic and heuristics
4. `services/` + `cli.py`: orchestration and user-facing commands

## Design decisions

### Standard library first

Use Python standard library HTTP and dotenv parsing to keep setup light.

### Domain analysis is independent from transport

Roast analysis consumes normalized datapoint dictionaries. The logic should remain usable with fixtures and future API changes.

### Crack analysis is cluster-aware

`crack` can contain isolated false positives. The analyzer must inspect the entire series, group nearby detections into clusters, rank clusters, and report ambiguity when signal quality is weak.

### Pragmatic onset vs active onset

The analyzer tracks both:

- practical onset: earliest cluster that looks like real first crack
- active onset: densest later cluster when the sequence becomes clearly active

This avoids overfitting to a single detection point.

## Deferred work

- richer machine-centric workflows
- plotting helpers
- export to CSV/parquet
- alternate heuristics tuned on more beans and machines
