from pathlib import Path
import numpy as np
import re
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

circuit_short_name = "Spa-Francorchamps"
debug = True
x = -3930
y = -1640
z = 0

def fileToArray(circuit_short_name):
    folder = Path("expy")
    folder.mkdir(exist_ok=True)
    file_path = folder / f"{circuit_short_name}.txt"

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

def to_xyz_array(coords):
    return np.array([
        [float(x), float(y), float(z) if z is not None else 0.0]
        for x, y, z in re.findall(
            r"x:\s*(-?\d+(?:\.\d+)?),\s*y:\s*(-?\d+(?:\.\d+)?)(?:,\s*z:\s*(-?\d+(?:\.\d+)?))?",
            "\n".join(coords),
        )
    ])

def xy2pct(x, y, z, circuit_short_name): #takes coordinates and finds the % along the track/pit lane it is
    track_coordinates, pit_lane_coordinates = fileToArray(circuit_short_name)
    track = to_xyz_array(track_coordinates)
    pit = to_xyz_array(pit_lane_coordinates)

    point = np.array([x, y, z])

    track_i = np.argmin(np.sum((track - point) ** 2, axis=1))
    pit_i = np.argmin(np.sum((pit - point) ** 2, axis=1))

    track_dist = np.sum((track[track_i] - point) ** 2)
    pit_dist = np.sum((pit[pit_i] - point) ** 2)

    onTrack = track_dist <= pit_dist

    coords = track if onTrack else pit
    index = track_i if onTrack else pit_i

    highlighted = coords[index]
    percentage = index / len(coords) * 100

    print(f"highlighted coordinate: x={highlighted[0]}, y={highlighted[1]}, z={highlighted[2]}")
    print(f"onTrack: {onTrack}")

    if debug:
        return onTrack, percentage, highlighted
    else:
        return onTrack, percentage

def plot(x, y, highlighted, track_coordinates, pit_lane_coordinates):
    track = to_xyz_array(track_coordinates)
    pit = to_xyz_array(pit_lane_coordinates)

    plt.scatter(track[:, 0], track[:, 1], color='blue', label='Track')
    plt.scatter(pit[:, 0], pit[:, 1], color='green', label='Pit Lane')
    plt.scatter(x, y, color='red', label='Input Point', zorder=5)
    plt.scatter(highlighted[0], highlighted[1], color='orange', label='Highlighted Point', zorder=5)
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
    plt.legend()
    plt.show()
    
    print(xy2pct(x, y, z, circuit_short_name))


if debug:
    plot(x, y, xy2pct(x, y, z, circuit_short_name)[2], *fileToArray(circuit_short_name))
