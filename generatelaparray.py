from urllib.request import urlopen
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pathlib import Path

circuit_short_name = 'Singapore'
clearanceGap = 50

# get session id, date start, and date end
def getSessionInfo(circuit_short_name):
    baselink = f'https://api.openf1.org/v1/sessions?circuit_short_name={circuit_short_name}&session_type=Qualifying&year=2025'
    response = urlopen(baselink)
    data = json.loads(response.read().decode('utf-8'))
    session_id = data[0]['session_key']
    date_start = data[0]['date_start']
    print(date_start)
    return session_id, date_start

# uses sessionid and start date to spit out array of coordinates in a lap
def getCoordinateArray(session_id, date_start):
    date_end = datetime.fromisoformat(date_start) + timedelta(minutes=30)
    coordinates = []
    link = f'https://api.openf1.org/v1/location?driver_number=4&session_key={session_id}&date>{date_start}&date<{date_end.isoformat()}'
    response = urlopen(link)
    data = json.loads(response.read().decode('utf-8'))
    for item in data:
        datapack = 'x: {x}, y: {y}, z: {z}'.format(x=item['x'], y=item['y'], z=item['z'])
        #delete all x=0 y=0 pairs
        if item['x'] == 0 and item['y'] == 0:
            continue
        #make it so that datapack checks that each x y pair is not in +-clearanceGap of any in coordinates
        is_unique = True
        for existing in coordinates:
            existing_x, existing_y, *_ = existing.split(', ')
            if abs(float(existing_x.split(': ')[1]) - float(item['x'])) <= clearanceGap and abs(float(existing_y.split(': ')[1]) - float(item['y'])) <= clearanceGap:
                is_unique = False
                break
        if is_unique:
            coordinates.append(datapack)
    return coordinates

# plots lap
def plot(coordinates):
    x_values = []
    y_values = []
    for coordinate in coordinates:
        x, y, *_ = coordinate.split(', ')
        x_values.append(float(x.split(': ')[1]))
        y_values.append(float(y.split(': ')[1]))
    #make first and last color red and the rest gradient from light blue to dark blue
    colors = ['red'] + [plt.cm.viridis(i) for i in np.linspace(0, 1, len(x_values) - 2)] + ['orange']
    for i in range(len(x_values)):
        plt.scatter(x_values[i], y_values[i], c=[colors[i]], marker='o')
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
    plt.title(f"{circuit_short_name} Lap Array")
    plt.show()

#generates file with track and pit lane coordinates
def exportToFile(coordinates, circuit_short_name):
    folder = Path("expy")
    folder.mkdir(exist_ok=True)
    filename = folder / f"{circuit_short_name}.txt"
    with open(filename, "w") as f:
        f.write("Track\n")
        f.write("\n".join(coordinates))
        f.write("\n\nPit Lane")
    


def generateLapArray():
    coordinatearray = getCoordinateArray(*getSessionInfo(circuit_short_name))
    exportToFile(coordinatearray, circuit_short_name)

    plot(coordinatearray)

generateLapArray()