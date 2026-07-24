import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

# Make direct execution use this checkout's package instead of an older installed copy.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from xy2pct.openf1 import get_json

allx = []
ally = []

data = get_json('https://api.openf1.org/v1/location?session_key=9939&date>2025-07-27T13:00:00.000&date<2025-07-27T13:20:00.000')
for each in data:
    allx.append(each['x'])
    ally.append(each['y'])



def plot(x, y):
    x_values = np.asarray(x)
    y_values = np.asarray(y)
    plt.plot(x_values, y_values, 'o') 
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
    plt.show()

    command = input("Type 'stop' to terminate: ")
    if command == 'stop':
        #stop application
        print("Terminating application.")
        exit()
    

plot(allx, ally)
