from __future__ import annotations

from pathlib import Path
from typing import Any
import html


def _fmt_label(seconds: float) -> str:
    total = int(round(seconds))
    return f"{total // 60}:{total % 60:02d}"


def _polyline_points(times: list[float], values: list[float | None], x0: float, y0: float, width: float, height: float) -> str:
    valid = [(t, v) for t, v in zip(times, values) if v is not None]
    if len(valid) < 2:
        return ""
    min_t = min(times) if times else 0.0
    max_t = max(times) if times else 1.0
    min_v = min(v for _, v in valid)
    max_v = max(v for _, v in valid)
    if max_t == min_t:
        max_t += 1.0
    if max_v == min_v:
        max_v += 1.0
    points = []
    for t, value in valid:
        x = x0 + ((t - min_t) / (max_t - min_t)) * width
        y = y0 + height - ((value - min_v) / (max_v - min_v)) * height
        points.append(f"{x:.1f},{y:.1f}")
    return " ".join(points)


def _line_x(time_s: float, times: list[float], x0: float, width: float) -> float:
    min_t = min(times) if times else 0.0
    max_t = max(times) if times else 1.0
    if max_t == min_t:
        max_t += 1.0
    return x0 + ((time_s - min_t) / (max_t - min_t)) * width


def write_roast_svg(
    series: dict[str, Any],
    output_path: Path,
    title: str,
    subtitle: str | None = None,
) -> None:
    width = 1200
    height = 880
    left = 80
    right = 40
    plot_width = width - left - right
    panel_height = 180
    gap = 70
    top = 80

    temp_y = top
    ror_y = temp_y + panel_height + gap
    control_y = ror_y + panel_height + gap
    crack_y = control_y + panel_height + gap
    times = series["time_s"]

    time_ticks = []
    if times:
        max_t = times[-1]
        step = max(30, int(max_t // 5) or 30)
        current = 0
        while current <= max_t:
            time_ticks.append(current)
            current += step
        if time_ticks[-1] != int(max_t):
            time_ticks.append(int(max_t))

    notes = series.get("notes", [])
    subtitle_text = subtitle or ""
    escaped_title = html.escape(title)
    escaped_subtitle = html.escape(subtitle_text)

    bean_poly = _polyline_points(times, series["bean_temp"], left, temp_y, plot_width, panel_height)
    inlet_poly = _polyline_points(times, series["inlet_temp"], left, temp_y, plot_width, panel_height)
    ror_poly = _polyline_points(times, series["ror30"], left, ror_y, plot_width, panel_height)
    heat_poly = _polyline_points(times, series["heat"], left, control_y, plot_width, panel_height)
    fan_poly = _polyline_points(times, series["fan"], left, control_y, plot_width, panel_height)
    crack_poly = _polyline_points(times, [point.get("crack_level", 0) for point in series["crack_points"]], left, crack_y, plot_width, panel_height)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>text{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;fill:#1f2937} .small{font-size:14px;fill:#4b5563} .label{font-size:16px;font-weight:600} .tick{font-size:12px;fill:#6b7280}</style>',
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="{left}" y="40" font-size="28" font-weight="700">{escaped_title}</text>',
        f'<text x="{left}" y="62" class="small">{escaped_subtitle}</text>',
    ]

    panels = [
        (temp_y, "Temperature", bean_poly, "#d97706", inlet_poly, "#2563eb"),
        (ror_y, "ROR30", ror_poly, "#7c3aed", "", "#000000"),
        (control_y, "Controls", heat_poly, "#dc2626", fan_poly, "#059669"),
        (crack_y, "Crack signal", crack_poly, "#111827", "", "#000000"),
    ]
    for y, label, primary, primary_color, secondary, secondary_color in panels:
        parts.append(f'<rect x="{left}" y="{y}" width="{plot_width}" height="{panel_height}" fill="#f9fafb" stroke="#e5e7eb"/>')
        parts.append(f'<text x="{left}" y="{y - 12}" class="label">{html.escape(label)}</text>')
        if primary:
            parts.append(f'<polyline fill="none" stroke="{primary_color}" stroke-width="3" points="{primary}"/>')
        if secondary:
            parts.append(f'<polyline fill="none" stroke="{secondary_color}" stroke-width="3" points="{secondary}"/>')
        for tick in time_ticks:
            x = _line_x(float(tick), times, left, plot_width)
            parts.append(f'<line x1="{x:.1f}" y1="{y}" x2="{x:.1f}" y2="{y + panel_height}" stroke="#e5e7eb" stroke-dasharray="4 4"/>')
            parts.append(f'<text x="{x:.1f}" y="{y + panel_height + 18}" text-anchor="middle" class="tick">{_fmt_label(float(tick))}</text>')

    for key, color in [("practical_onset", "#b45309"), ("active_onset", "#7c2d12")]:
        onset = series.get(key)
        if onset:
            x = _line_x(float(onset["time_s"]), times, left, plot_width)
            parts.append(f'<line x1="{x:.1f}" y1="{temp_y}" x2="{x:.1f}" y2="{crack_y + panel_height}" stroke="{color}" stroke-width="2" stroke-dasharray="8 6"/>')
            parts.append(f'<text x="{x + 6:.1f}" y="{temp_y + 16}" class="small">{html.escape(key)}</text>')

    for point in series.get("crack_points", []):
        x = _line_x(float(point["time_s"]), times, left, plot_width)
        parts.append(f'<circle cx="{x:.1f}" cy="{crack_y + panel_height/2:.1f}" r="4" fill="#111827"/>')

    legend_y = crack_y + panel_height + 48
    legend = [
        ("Bean temp", "#d97706"),
        ("Inlet temp", "#2563eb"),
        ("ROR30", "#7c3aed"),
        ("Heat", "#dc2626"),
        ("Fan", "#059669"),
    ]
    x = left
    for label, color in legend:
        parts.append(f'<line x1="{x}" y1="{legend_y}" x2="{x + 24}" y2="{legend_y}" stroke="{color}" stroke-width="4"/>')
        parts.append(f'<text x="{x + 32}" y="{legend_y + 5}" class="small">{html.escape(label)}</text>')
        x += 160

    note_y = legend_y + 32
    for note in notes[:4]:
        parts.append(f'<text x="{left}" y="{note_y}" class="small">• {html.escape(note)}</text>')
        note_y += 20

    parts.append('</svg>')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(parts))
