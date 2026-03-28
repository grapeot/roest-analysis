from __future__ import annotations

from typing import Any

from ..analysis.crack_detection import analyze_crack_signal
from ..analysis.phase_metrics import compute_phase_metrics
from ..analysis.summarize import render_text_summary
from ..api.client import RoestApiClient


def analyze_log_id(client: RoestApiClient, log_id: int) -> dict[str, Any]:
    bundle = client.get_log_bundle(log_id)
    crack_analysis = analyze_crack_signal(bundle.datapoints)
    metrics = compute_phase_metrics(bundle.datapoints, crack_analysis)
    result: dict[str, Any] = {
        "log_id": log_id,
        "log": bundle.log,
        "crack_analysis": crack_analysis,
        "metrics": metrics,
    }
    result["summary_text"] = render_text_summary(result)
    return result
