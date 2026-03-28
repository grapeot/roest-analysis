# Roest Analysis Skill

## Goal

Fetch Roest roast logs and analyze them in a way that matches actual roasting diagnostics, not just raw API events.

## Canonical location

- Project-local source of truth: `adhoc_jobs/roest_analysis/skills/roest_analysis.md`
- Global wrapper: `rules/skills/roest_analysis.md`

If you are reading this from the global skills system, this project lives at `adhoc_jobs/roest_analysis/`.

## Workflow

1. Check `.env` in the project root for `ROEST_API_TOKEN`
2. Use the CLI to fetch the log and datapoints by log ID
3. Analyze crack detections as a full sequence, not as a first-hit trigger
4. Use practical onset and active cluster together when diagnosing development
5. Compare roast metrics across multiple roasts before drawing conclusions

## CLI usage

```bash
python -m roest_analysis.cli doctor config
python -m roest_analysis.cli log fetch --log-id 3598310 --resource bundle --format json
python -m roest_analysis.cli log analyze --log-id 3598319 --format text
python -m roest_analysis.cli machine logs --machine-id 2559
python -m roest_analysis.cli machine slots --machine-id 2559
python -m roest_analysis.cli machine flagged-logs --machine-id 2559 --event-flags 36
```

## Analysis rules

### Do not trust the first crack point

Roest `crack` appears to be a detection stream, not a perfect ground-truth event marker. A single early point can be noise or an isolated early pop.

### Look at all crack points and cluster them

- Collect every non-zero `crack` datapoint
- Group nearby points into clusters
- Separate isolated early points from sustained later clusters
- Prefer a practical onset that comes from a meaningful cluster, not a lone spike
- Track the strongest later cluster as active crack phase

### Keep ambiguity explicit

If multiple crack clusters are similarly strong, say the signal is ambiguous. Do not force a fake exact onset.

## Common pitfalls

- Using the first non-zero `crack` datapoint as first crack
- Treating API-derived first crack as equivalent to audible first crack
- Looking only at one roast instead of comparing neighboring experiments
- Ignoring heat/fan control changes around crack
- Printing or pasting the raw bearer token in logs or outputs

## Project notes

- Token comes from `adhoc_jobs/roest_analysis/.env`
- The CLI only needs a log ID for the main fetch/analyze path
- API coverage currently includes log detail, datapoints, machine slots, and filtered logs by event flags
