from xy2pct import givetrackarray


def test_givetrackarray_returns_track_and_pit_points():
    track_points, pit_track_points = givetrackarray("Singapore")

    assert track_points
    assert pit_track_points
    assert track_points[0].startswith("x: ")
    assert pit_track_points[0].startswith("x: ")


def test_givetrackarray_raw_returns_complete_file():
    raw_file = givetrackarray("Singapore", raw=True)

    assert raw_file.startswith("Track\n")
    assert "Pit Lane" in raw_file
