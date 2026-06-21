from urllib.request import urlopen
import json
import numpy as np
import matplotlib.pyplot as plt

allx = []
ally = []

response = urlopen('https://api.openf1.org/v1/location?session_key=9939&date>2025-07-27T13:00:00.000&date<2025-07-27T13:20:00.000')
data = json.loads(response.read().decode('utf-8'))
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
