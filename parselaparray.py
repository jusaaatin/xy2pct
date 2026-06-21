from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

countryName = "Singapore"


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


def draw_plot(ax, track_coordinates, pit_lane_coordinates):
    ax.clear()

    x_values = []
    y_values = []

    for coordinate in track_coordinates:
        x, y = coordinate.split(", ")
        x_values.append(float(x.split(": ")[1]))
        y_values.append(float(y.split(": ")[1]))

    for coordinate in pit_lane_coordinates:
        x, y = coordinate.split(", ")
        x_values.append(float(x.split(": ")[1]))
        y_values.append(float(y.split(": ")[1]))

    point_colors = (
        [plt.cm.winter(i) for i in np.linspace(0, 1, len(track_coordinates))]
        + [plt.cm.autumn(i) for i in np.linspace(0, 1, len(pit_lane_coordinates))]
    )

    for i in range(len(x_values)):
        ax.scatter(x_values[i], y_values[i], c=[point_colors[i]], marker="o")

    ax.axhline(0, color="black", linewidth=0.5, linestyle="--")
    ax.axvline(0, color="black", linewidth=0.5, linestyle="--")
    ax.set_title(f"{countryName} Track and Pit Lane")


def plot(countryName):
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)

    track_coordinates, pit_lane_coordinates = fileToArray(countryName)
    draw_plot(ax, track_coordinates, pit_lane_coordinates)

    button_ax = plt.axes([0.4, 0.05, 0.2, 0.075])
    reload_button = Button(button_ax, "Reload")

    def reload(event):
        track_coordinates, pit_lane_coordinates = fileToArray(countryName)
        draw_plot(ax, track_coordinates, pit_lane_coordinates)
        fig.canvas.draw_idle()

    reload_button.on_clicked(reload)

    plt.show()


plot(countryName)