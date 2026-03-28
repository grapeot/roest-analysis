from __future__ import annotations

from typing import Any


def _time_s(point: dict[str, Any]) -> float:
    raw = point.get("msec", point.get("ms", point.get("time")))
    if raw is None:
        raise ValueError("Datapoint is missing time field.")
    return float(raw) / 1000.0


def _bt(point: dict[str, Any]) -> float | None:
    value = point.get("bt", point.get("bean_temp", point.get("beanTemperature")))
    if value is None:
        return None
    return float(value)


def _ror30(datapoints: list[dict[str, Any]], index: int) -> float | None:
    current = datapoints[index]
    current_bt = _bt(current)
    if current_bt is None:
        return None
    current_t = _time_s(current)
    previous_index = 0
    for idx in range(index, -1, -1):
        if current_t - _time_s(datapoints[idx]) >= 30:
            previous_index = idx
            break
    previous = datapoints[previous_index]
    previous_bt = _bt(previous)
    if previous_bt is None:
        return None
    dt = current_t - _time_s(previous)
    if dt <= 0:
        return None
    return (current_bt - previous_bt) / dt


def compute_phase_metrics(
    datapoints: list[dict[str, Any]],
    crack_analysis: dict[str, Any],
) -> dict[str, Any]:
    if not datapoints:
        raise ValueError("datapoints cannot be empty")

    valid = [point for point in datapoints if _bt(point) is not None]
    turning_point = min(valid, key=lambda point: _bt(point) or 0)
    drop = valid[-1]
    tp_index = valid.index(turning_point)
    yellow = next(
        (point for point in valid[tp_index:] if (_bt(point) or 0) >= 150.0),
        None,
    )

    practical_onset = crack_analysis.get("practical_onset")
    onset_time_s = practical_onset["time_s"] if practical_onset else None
    onset_point = None
    onset_index = None
    if onset_time_s is not None:
        onset_index = min(
            range(len(valid)), key=lambda idx: abs(_time_s(valid[idx]) - onset_time_s)
        )
        onset_point = valid[onset_index]

    metrics: dict[str, Any] = {
        "total_time_s": _time_s(drop),
        "turning_point": {
            "time_s": _time_s(turning_point),
            "bt": _bt(turning_point),
        },
        "yellow": (
            {"time_s": _time_s(yellow), "bt": _bt(yellow)} if yellow is not None else None
        ),
        "drop": {"time_s": _time_s(drop), "bt": _bt(drop)},
    }

    if onset_point is not None and onset_index is not None:
        development_time_s = _time_s(drop) - _time_s(onset_point)
        metrics["practical_onset"] = {
            "time_s": _time_s(onset_point),
            "bt": _bt(onset_point),
            "ror30": _ror30(valid, onset_index),
        }
        metrics["development"] = {
            "time_s": development_time_s,
            "ratio": development_time_s / _time_s(drop),
            "delta_bt": (_bt(drop) or 0.0) - (_bt(onset_point) or 0.0),
        }
    else:
        metrics["practical_onset"] = None
        metrics["development"] = None

    return metrics
