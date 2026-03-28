from roest_analysis.analysis.crack_detection import analyze_crack_signal


def test_isolated_first_point_is_treated_as_outlier():
    datapoints = [
        {"msec": 270000, "bt": 193.5, "crack": 1},
        {"msec": 294000, "bt": 201.6, "crack": 1},
        {"msec": 300000, "bt": 203.6, "crack": 1},
        {"msec": 313000, "bt": 207.4, "crack": 2},
        {"msec": 314000, "bt": 207.7, "crack": 1},
        {"msec": 315000, "bt": 208.0, "crack": 1},
    ]

    result = analyze_crack_signal(datapoints)

    assert result["practical_onset"]["time_s"] == 294.0
    assert result["active_onset"]["time_s"] == 313.0
    assert result["outlier_points"][0]["time_s"] == 270.0


def test_no_crack_points_is_ambiguous():
    result = analyze_crack_signal([{"msec": 0, "bt": 205.0, "crack": 0}])

    assert result["practical_onset"] is None
    assert result["ambiguous"] is True


def test_split_clusters_are_marked_ambiguous():
    datapoints = [
        {"msec": 270000, "bt": 193.5, "crack": 1},
        {"msec": 294000, "bt": 201.6, "crack": 1},
        {"msec": 300000, "bt": 203.6, "crack": 1},
        {"msec": 313000, "bt": 207.4, "crack": 2},
        {"msec": 314000, "bt": 207.7, "crack": 1},
        {"msec": 315000, "bt": 208.0, "crack": 1},
        {"msec": 318000, "bt": 208.8, "crack": 1},
    ]

    result = analyze_crack_signal(datapoints)

    assert result["ambiguous"] is True
    assert any("conservatively" in note for note in result["notes"])
