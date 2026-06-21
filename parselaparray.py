from pathlib import Path
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt

countryName = 'Singapore'



def fileToArray(countryName):
    folder = Path("expy")
    folder.mkdir(exist_ok=True)
    file_path = folder / f"{countryName}.txt"
    if not file_path.exists():
        print(f"File {file_path} does not exist.")
        return []
    with open(file_path, 'r') as file:
        #create 2 arrays: 1 for all after "Track" and 1 for all after "Pit Lane"
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

def plot(track_coordinates, pit_lane_coordinates):
    x_values = []
    y_values = []
    for coordinate in track_coordinates:
        x, y = coordinate.split(', ')
        x_values.append(float(x.split(': ')[1]))
        y_values.append(float(y.split(': ')[1]))
    for coordinate in pit_lane_coordinates:
        x, y = coordinate.split(', ')
        x_values.append(float(x.split(': ')[1]))
        y_values.append(float(y.split(': ')[1]))
    #track coordinates are blue and pit lane are red with a gradient from light to dark
    colors = [plt.cm.winter(i) for i in np.linspace(0, 1, len(track_coordinates))] + [plt.cm.autumn(i) for i in np.linspace(0, 1, len(pit_lane_coordinates))]
    for i in range(len(x_values)):
        plt.scatter(x_values[i], y_values[i], c=[colors[i]], marker='o')
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
    plt.title(f"{countryName} Track and Pit Lane")
    plt.show()


plot(*fileToArray(countryName))