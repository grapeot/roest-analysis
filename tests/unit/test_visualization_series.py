from roest_analysis.analysis.crack_detection import analyze_crack_signal
from roest_analysis.visualization.series import build_plot_series


def test_build_plot_series_extracts_core_signals():
    datapoints = [
        {"msec": 0, "bt": 205.0, "inlet_temp": 230.0, "heat": 40, "fan": 43, "crack": 0},
        {"msec": 30000, "bt": 150.0, "tc1": 220.0, "heat": 50, "fan": 44, "crack": 0},
        {"msec": 60000, "bt": 180.0, "inlet_temp": 240.0, "heat": 55, "fan": 45, "crack": 1},
    ]

    crack_analysis = analyze_crack_signal(datapoints)
    series = build_plot_series(datapoints, crack_analysis)

    assert series["time_s"] == [0.0, 30.0, 60.0]
    assert series["bean_temp"] == [205.0, 150.0, 180.0]
    assert series["inlet_temp"] == [230.0, 220.0, 240.0]
    assert series["heat"] == [40.0, 50.0, 55.0]
    assert series["fan"] == [43.0, 44.0, 45.0]
    assert series["crack_points"][0]["time_s"] == 60.0


def test_build_plot_series_handles_missing_inlet_temperature():
    datapoints = [
        {"msec": 0, "bt": 200.0, "heat": 40, "fan": 43, "crack": 0},
        {"msec": 30000, "bt": 150.0, "heat": 50, "fan": 44, "crack": 0},
        {"msec": 60000, "bt": 180.0, "heat": 55, "fan": 45, "crack": 1},
    ]

    crack_analysis = analyze_crack_signal(datapoints)
    series = build_plot_series(datapoints, crack_analysis)

    assert series["inlet_temp"] == [None, None, None]
    assert series["notes"]
