from pathlib import Path


TRACK_DATA_DIRECTORY = Path("src/xy2pct/expy")


def _read_track_file(file_path: Path) -> tuple[str, list[str], list[str]]:
    file_contents = file_path.read_text(encoding="utf-8")
    track_points = []
    pit_track_points = []
    current_section = None

    for line in file_contents.splitlines():
        line = line.strip()

        if not line:
            continue
        if line == "Track":
            current_section = "track"
        elif line == "Pit Lane":
            current_section = "pit_track"
        elif current_section == "track":
            track_points.append(line)
        elif current_section == "pit_track":
            pit_track_points.append(line)

    return file_contents, track_points, pit_track_points


def givetrackarray(
    circuit_name: str,
    raw: bool | None = None,
) -> list[object] | str:
    if circuit_name == "*":
        file_paths = sorted(TRACK_DATA_DIRECTORY.glob("*.txt"))
        if not file_paths:
            return []

        all_tracks = []
        for file_path in file_paths:
            file_contents, track_points, pit_track_points = _read_track_file(file_path)
            if raw is True:
                all_tracks.extend([file_path.stem, file_contents])
            else:
                all_tracks.extend([file_path.stem, track_points, pit_track_points])
        return all_tracks

    file_path = TRACK_DATA_DIRECTORY / f"{circuit_name}.txt"
    if not file_path.is_file():
        raise FileNotFoundError(
            f"Track '{circuit_name}' not found ({file_path})."
        )

    file_contents, track_points, pit_track_points = _read_track_file(file_path)
    if raw is True:
        return file_contents

    return [circuit_name, track_points, pit_track_points]
