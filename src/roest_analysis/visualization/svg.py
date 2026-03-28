from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def _format_seconds(seconds: float) -> str:
    total = int(round(seconds))
    return f"{total // 60}:{total % 60:02d}"


def _valid_pairs(times: list[float], values: list[float | None]) -> tuple[list[float], list[float]]:
    valid = [(time_s, value) for time_s, value in zip(times, values) if value is not None]
    if not valid:
        return [], []
    xs, ys = zip(*valid, strict=False)
    return list(xs), list(ys)


def _set_time_axis(axis: Any, times: list[float]) -> None:
    if not times:
        axis.set_xlabel("Time")
        return

    max_t = max(times)
    tick_count = 6
    if max_t <= 0:
        ticks = [0]
    else:
        ticks = [max_t * index / (tick_count - 1) for index in range(tick_count)]
    axis.set_xticks(ticks)
    axis.set_xticklabels([_format_seconds(tick) for tick in ticks])
    axis.set_xlabel("Time")


def _annotate_onset(axis: Any, onset: dict[str, Any] | None, color: str, label: str) -> None:
    if not onset:
        return
    time_s = float(onset["time_s"])
    axis.axvline(time_s, color=color, linestyle="--", linewidth=1.6, alpha=0.9)
    ymin, ymax = axis.get_ylim()
    axis.text(
        time_s + (max(time_s * 0.01, 2.0)),
        ymax - ((ymax - ymin) * 0.08),
        label,
        color=color,
        fontsize=9,
        va="top",
    )


def write_roast_svg(
    series: dict[str, Any],
    output_path: Path,
    title: str,
    subtitle: str | None = None,
) -> None:
    times = [float(time_s) for time_s in series["time_s"]]
    bean_x, bean_y = _valid_pairs(times, series["bean_temp"])
    inlet_x, inlet_y = _valid_pairs(times, series["inlet_temp"])
    ror_x, ror_y = _valid_pairs(times, series["ror30"])
    heat_x, heat_y = _valid_pairs(times, series["heat"])
    fan_x, fan_y = _valid_pairs(times, series["fan"])

    crack_points = series.get("crack_points", [])
    crack_x = [float(point["time_s"]) for point in crack_points]
    crack_y = [float(point.get("crack_level", 0)) for point in crack_points]

    figure, axes = plt.subplots(
        nrows=4,
        ncols=1,
        figsize=(14, 12),
        sharex=True,
        constrained_layout=True,
    )

    figure.suptitle(title, fontsize=20, fontweight="bold")
    if subtitle:
        figure.text(0.125, 0.965, subtitle, fontsize=11)

    temperature_axis, ror_axis, control_axis, crack_axis = axes

    if bean_x:
        temperature_axis.plot(bean_x, bean_y, color="#d97706", linewidth=2.2, label="Bean temp")
    if inlet_x:
        temperature_axis.plot(inlet_x, inlet_y, color="#2563eb", linewidth=2.2, label="Inlet temp")
    temperature_axis.set_title("Temperature", loc="left", fontsize=13, fontweight="bold")
    temperature_axis.set_ylabel("°C")
    temperature_axis.grid(True, axis="both", linestyle="--", alpha=0.25)
    if bean_x or inlet_x:
        temperature_axis.legend(loc="upper left")

    if ror_x:
        ror_axis.plot(ror_x, ror_y, color="#7c3aed", linewidth=2.2, label="ROR30")
    ror_axis.set_title("ROR30", loc="left", fontsize=13, fontweight="bold")
    ror_axis.set_ylabel("°C/min")
    ror_axis.set_ylim(bottom=0)
    ror_axis.grid(True, axis="both", linestyle="--", alpha=0.25)
    if ror_x:
        ror_axis.legend(loc="upper left")

    if heat_x:
        control_axis.plot(heat_x, heat_y, color="#dc2626", linewidth=2.2, label="Heat")
    if fan_x:
        control_axis.plot(fan_x, fan_y, color="#059669", linewidth=2.2, label="Fan")
    control_axis.set_title("Controls", loc="left", fontsize=13, fontweight="bold")
    control_axis.set_ylabel("%")
    control_axis.set_ylim(-2, 102)
    control_axis.grid(True, axis="both", linestyle="--", alpha=0.25)
    if heat_x or fan_x:
        control_axis.legend(loc="upper left")

    if crack_x:
        crack_axis.plot(crack_x, crack_y, color="#111827", linewidth=1.5, alpha=0.7)
        crack_axis.scatter(crack_x, crack_y, color="#111827", s=28, zorder=3)
    crack_axis.set_title("Crack signal", loc="left", fontsize=13, fontweight="bold")
    crack_axis.set_ylabel("level")
    crack_axis.set_ylim(-0.1, max(2.1, max(crack_y) + 0.3 if crack_y else 2.1))
    crack_axis.set_yticks([0, 1, 2])
    crack_axis.grid(True, axis="both", linestyle="--", alpha=0.25)

    for axis in axes:
        _annotate_onset(axis, series.get("practical_onset"), "#b45309", "practical onset")
        _annotate_onset(axis, series.get("active_onset"), "#7c2d12", "active onset")
        if times:
            axis.set_xlim(min(times), max(times))

    _set_time_axis(crack_axis, times)

    notes = series.get("notes", [])
    if notes:
        notes_text = "\n".join(f"• {note}" for note in notes[:4])
        figure.text(0.125, 0.015, notes_text, fontsize=9, va="bottom")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, format="svg")
    plt.close(figure)
