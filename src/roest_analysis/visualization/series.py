from __future__ import annotations

from typing import Any


def _time_s(point: dict[str, Any]) -> float:
    raw = point.get("msec", point.get("ms", point.get("time")))
    if raw is None:
        raise ValueError("Datapoint is missing time field.")
    return float(raw) / 1000.0


def _as_float(value: Any) -> float | None:
    if value is None:
        return None
    return float(value)


def _bean_temp(point: dict[str, Any]) -> float | None:
    return _as_float(point.get("bt", point.get("bean_temp", point.get("beanTemperature"))))


def _inlet_temp(point: dict[str, Any]) -> float | None:
    return _as_float(point.get("inlet_temp", point.get("tc1", point.get("inletTemperature"))))


def _control(point: dict[str, Any], key: str) -> float | None:
    return _as_float(point.get(key))


def _ror30(datapoints: list[dict[str, Any]], index: int) -> float | None:
    current = datapoints[index]
    current_bt = _bean_temp(current)
    if current_bt is None:
        return None
    current_t = _time_s(current)
    previous_index = 0
    for idx in range(index, -1, -1):
        if current_t - _time_s(datapoints[idx]) >= 30:
            previous_index = idx
            break
    previous = datapoints[previous_index]
    previous_bt = _bean_temp(previous)
    if previous_bt is None:
        return None
    dt = current_t - _time_s(previous)
    if dt <= 0:
        return None
    return ((current_bt - previous_bt) / dt) * 60.0


def build_plot_series(datapoints: list[dict[str, Any]], crack_analysis: dict[str, Any]) -> dict[str, Any]:
    if not datapoints:
        raise ValueError("datapoints cannot be empty")

    time_s = [_time_s(point) for point in datapoints]
    bean_temp = [_bean_temp(point) for point in datapoints]
    inlet_temp = [_inlet_temp(point) for point in datapoints]
    heat = [_control(point, "heat") for point in datapoints]
    fan = [_control(point, "fan") for point in datapoints]
    ror30 = [_ror30(datapoints, idx) for idx in range(len(datapoints))]
    positive_started = False
    normalized_ror30: list[float | None] = []
    for value in ror30:
        if value is None:
            normalized_ror30.append(None)
            continue
        if not positive_started:
            if value >= 0:
                positive_started = True
                normalized_ror30.append(value)
            else:
                normalized_ror30.append(None)
        else:
            normalized_ror30.append(value)

    notes: list[str] = []
    if all(value is None for value in inlet_temp):
        notes.append("Inlet temperature was missing; the chart omits that series.")

    return {
        "time_s": time_s,
        "bean_temp": bean_temp,
        "inlet_temp": inlet_temp,
        "heat": heat,
        "fan": fan,
        "ror30": normalized_ror30,
        "crack_points": crack_analysis.get("points", []),
        "practical_onset": crack_analysis.get("practical_onset"),
        "active_onset": crack_analysis.get("active_onset"),
        "notes": notes + list(crack_analysis.get("notes", [])),
    }
