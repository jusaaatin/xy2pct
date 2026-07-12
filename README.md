# xy2pct
A tool that pinpoints the percentage along a predetermined track of given coordinates.

## Installation

To install the Python package, run:

```
pip install xy2pct
```

## Workflow

### Create track map 
1. create an "expy" folder in the same directory as your current python file
2. use [generatelaparray.py](https://github.com/jusaaatin/f1-xy2pct/blob/main/generatelaparray.py) to spit out a file with x, y, and z coordinates for the track. The data will appear in '(circuit_short_name).json'.
3. manually delete extra data points and assign relevant ones to pit lane by moving them under "Pit Lane:"
4. use [parselaparray.py](https://github.com/jusaaatin/f1-xy2pct/blob/main/parselaparray.py) to check work (sample code to also go from file to array)


### Use xy2pct
```
def xy2pct(x, y, z, circuit_short_name) -> [onTrack, percentage]
```
1. use the function xy2pct(x, y, z, circuit_short_name) to convert any x, y, and z(optional) to a percentage along the track you specify in circuit_short_name. to find the variable, use the openf1 docs: https://api.openf1.org/v1/meetings?year=2026&country_name=Singapore and replace the country name with the one you want, and then find the name beside `circuit_short_name`.
