from pathlib import Path
import numpy as np
import re

countryName = "Singapore"
x = 850
y = 0

def fileToArray(countryName):
    folder = Path("expy")
    folder.mkdir(exist_ok=True)
    file_path = folder / f"{countryName}.txt"

    if not file_path.exists():
        print(f"File {file_path} does not exist.")
        return [], []

    with open(file_path, "r") as file:
        lines = file.readlines()

    track_coordinates = []
    pit_lane_coordinates = []
    current_section = None

    for line in lines:
        line = line.strip()

        if line == "":
            continue
        if line == "Track":
            current_section = "track"
        elif line == "Pit Lane":
            current_section = "pit_lane"
        elif current_section == "track":
            track_coordinates.append(line)
        elif current_section == "pit_lane":
            pit_lane_coordinates.append(line)

    return track_coordinates, pit_lane_coordinates

def to_xy_array(coords):
    return np.array([
        [float(x), float(y)]
        for x, y in re.findall(r"x:\s*(-?\d+(?:\.\d+)?),\s*y:\s*(-?\d+(?:\.\d+)?)", "\n".join(coords))
    ])

def xy2pct(x, y, track_coordinates, pit_lane_coordinates):
    track = to_xy_array(track_coordinates)
    pit = to_xy_array(pit_lane_coordinates)

    point = np.array([x, y])

    track_i = np.argmin(np.sum((track - point) ** 2, axis=1))
    pit_i = np.argmin(np.sum((pit - point) ** 2, axis=1))

    track_dist = np.sum((track[track_i] - point) ** 2)
    pit_dist = np.sum((pit[pit_i] - point) ** 2)

    onTrack = track_dist <= pit_dist

    coords = track if onTrack else pit
    index = track_i if onTrack else pit_i

    highlighted = coords[index]
    percentage = index / len(coords) * 100

    print(f"highlighted coordinate: x={highlighted[0]}, y={highlighted[1]}")
    print(f"onTrack: {onTrack}")

    return onTrack, percentage


print(xy2pct(x, y, *fileToArray(countryName)))