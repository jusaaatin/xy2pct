from pathlib import Path


TRACK_DATA_DIRECTORY = Path("src/xy2pct/expy")


def givetrackarray(
    circuit_name: str,
    raw: bool | None = None,
) -> tuple[list[str], list[str]] | str:
    file_path = TRACK_DATA_DIRECTORY / f"{circuit_name}.txt"

    if not file_path.is_file():
        raise FileNotFoundError(
            f"Track '{circuit_name}' not found ({file_path})."
        )

    file_contents = file_path.read_text(encoding="utf-8")
    if raw is True:
        return file_contents

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

    return track_points, pit_track_points
