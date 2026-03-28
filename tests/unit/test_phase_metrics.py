from roest_analysis.analysis.crack_detection import analyze_crack_signal
from roest_analysis.analysis.phase_metrics import compute_phase_metrics


def test_phase_metrics_use_practical_onset():
    datapoints = [
        {"msec": 0, "bt": 205.0, "crack": 0},
        {"msec": 30000, "bt": 120.0, "crack": 0},
        {"msec": 60000, "bt": 90.0, "crack": 0},
        {"msec": 150000, "bt": 150.0, "crack": 0},
        {"msec": 270000, "bt": 193.5, "crack": 1},
        {"msec": 294000, "bt": 201.6, "crack": 1},
        {"msec": 300000, "bt": 203.6, "crack": 1},
        {"msec": 330000, "bt": 213.8, "crack": 0},
    ]

    crack_analysis = analyze_crack_signal(datapoints)
    metrics = compute_phase_metrics(datapoints, crack_analysis)

    assert metrics["turning_point"]["time_s"] == 60.0
    assert metrics["yellow"]["time_s"] == 150.0
    assert metrics["practical_onset"]["time_s"] == 294.0
    assert round(metrics["development"]["time_s"], 1) == 36.0
