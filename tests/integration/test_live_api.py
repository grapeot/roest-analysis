import pytest

from roest_analysis.analysis.crack_detection import analyze_crack_signal
from roest_analysis.analysis.phase_metrics import compute_phase_metrics
from roest_analysis.api.client import RoestApiClient
from roest_analysis.config import load_settings
from roest_analysis.errors import ConfigurationError


@pytest.mark.live_integration
def test_live_log_fetch_and_datapoints():
    try:
        settings = load_settings()
    except ConfigurationError:
        pytest.skip("ROEST_API_TOKEN is not configured")
    if not settings.enable_live_tests:
        pytest.skip("ROEST_ENABLE_LIVE_TESTS is not enabled")
    if settings.machine_id is None:
        pytest.skip("ROEST_MACHINE_ID is not configured")
    client = RoestApiClient(settings)
    logs = client.get_logs(machine_id=settings.machine_id)
    items = logs["results"] if isinstance(logs, dict) and "results" in logs else logs
    completed = [entry for entry in items if entry.get("drop_timestamp")]
    assert completed
    log_id = completed[0]["id"]
    log = client.get_log(log_id)
    datapoints = client.get_datapoints(log_id)
    assert log["id"] == log_id
    assert isinstance(datapoints, list)
    assert datapoints


@pytest.mark.live_integration
def test_live_list_logs_and_analyze_first_three():
    try:
        settings = load_settings()
    except ConfigurationError:
        pytest.skip("ROEST_API_TOKEN is not configured")
    if not settings.enable_live_tests:
        pytest.skip("ROEST_ENABLE_LIVE_TESTS is not enabled")

    client = RoestApiClient(settings)
    if settings.machine_id is None:
        pytest.skip("ROEST_MACHINE_ID is not configured")

    logs = client.get_logs(machine_id=settings.machine_id)

    if isinstance(logs, dict) and "results" in logs:
        items = logs["results"]
    else:
        items = logs

    assert isinstance(items, list)
    assert len(items) >= 3

    for entry in items[:3]:
        log_id = entry["id"]
        datapoints = client.get_datapoints(log_id)
        crack = analyze_crack_signal(datapoints)
        metrics = compute_phase_metrics(datapoints, crack)

        assert datapoints
        assert metrics["total_time_s"] > 0
        assert "clusters" in crack
