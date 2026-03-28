from __future__ import annotations

from pathlib import Path

from ..analysis.crack_detection import analyze_crack_signal
from ..api.client import RoestApiClient
from ..visualization.series import build_plot_series
from ..visualization.svg import write_roast_svg


def plot_log_id(
    client: RoestApiClient,
    log_id: int,
    output_path: Path,
    title: str | None = None,
) -> dict[str, str]:
    bundle = client.get_log_bundle(log_id)
    crack_analysis = analyze_crack_signal(bundle.datapoints)
    series = build_plot_series(bundle.datapoints, crack_analysis)
    chart_title = title or f"Roast overview: log {log_id}"
    subtitle = f"Practical onset {crack_analysis['practical_onset']['time_s']:.0f}s" if crack_analysis.get('practical_onset') else "No crack onset detected"
    write_roast_svg(series, output_path=output_path, title=chart_title, subtitle=subtitle)
    return {"output_path": str(output_path)}
