from __future__ import annotations

from typing import Any


def _fmt_time(seconds: float | None) -> str:
    if seconds is None:
        return "n/a"
    total = int(round(seconds))
    return f"{total // 60}:{total % 60:02d}"


def render_text_summary(result: dict[str, Any]) -> str:
    metrics = result["metrics"]
    crack = result["crack_analysis"]
    development = metrics.get("development")
    active_development = metrics.get("active_development")
    practical = metrics.get("practical_onset")
    active_onset = metrics.get("active_onset")

    lines = [
        f"Log ID: {result['log_id']}",
        f"Total time: {_fmt_time(metrics['total_time_s'])}",
        f"Turning point: {_fmt_time(metrics['turning_point']['time_s'])} / BT {metrics['turning_point']['bt']:.1f}",
    ]
    if metrics.get("yellow"):
        lines.append(
            f"Yellow (~150C): {_fmt_time(metrics['yellow']['time_s'])} / BT {metrics['yellow']['bt']:.1f}"
        )
    if practical:
        lines.append(
            f"Practical crack onset: {_fmt_time(practical['time_s'])} / BT {practical['bt']:.1f} / ROR30 {practical['ror30']:.3f}"
        )
    if development:
        lines.append(
            f"Development: {_fmt_time(development['time_s'])} / {development['ratio'] * 100:.1f}% / ΔBT {development['delta_bt']:.1f}"
        )
    if active_onset:
        lines.append(
            f"Active crack onset: {_fmt_time(active_onset['time_s'])} / BT {active_onset['bt']:.1f} / ROR30 {active_onset['ror30']:.3f}"
        )
    if active_development:
        lines.append(
            f"Active-cluster development: {_fmt_time(active_development['time_s'])} / {active_development['ratio'] * 100:.1f}% / ΔBT {active_development['delta_bt']:.1f}"
        )
    lines.append(f"Crack clusters: {len(crack['clusters'])}")
    if crack.get("outlier_points"):
        outlier_times = ", ".join(_fmt_time(point['time_s']) for point in crack['outlier_points'])
        lines.append(f"Outlier crack points ignored for onset: {outlier_times}")
    if crack.get("active_onset"):
        lines.append(
            f"Active crack cluster: {_fmt_time(crack['active_onset']['time_s'])} / BT {crack['active_onset']['bt']:.1f}"
        )
    if crack.get("notes"):
        lines.extend(f"Note: {note}" for note in crack['notes'])
    return "\n".join(lines)
