from xy2pct import givetrackarray


def test_givetrackarray_returns_track_and_pit_points():
    result = givetrackarray("Singapore")
    track_points, pit_track_points = result[1:]

    assert result[0] == "Singapore"
    assert track_points
    assert pit_track_points
    assert track_points[0].startswith("x: ")
    assert pit_track_points[0].startswith("x: ")


def test_givetrackarray_raw_returns_complete_file():
    raw_file = givetrackarray("Singapore", raw=True)

    assert raw_file.startswith("Track\n")
    assert "Pit Lane" in raw_file


def test_givetrackarray_wildcard_returns_all_maps():
    result = givetrackarray("*")

    assert result[::3] == ["Hungaroring", "Singapore", "Spa-Francorchamps"]
    assert all(result[index] for index in range(1, len(result), 3))
    assert all(result[index] for index in range(2, len(result), 3))
