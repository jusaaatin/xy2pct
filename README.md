workflow:

CREATE track map
1. use [generatelaparray.py](https://github.com/jusaaatin/f1-xy2pct/blob/main/generatelaparray.py) to spit out a file with x, y, and z coordinates for the track. The data will appear in (circuit_short_name).json.
2. manually delete extra data points and assign relevant ones to pit lane by moving them under "Pit Lane:"
3. use [parselaparray.py](https://github.com/jusaaatin/f1-xy2pct/blob/main/parselaparray.py) to check work (sample code to also go from file to array)


USE xy2pct
1. use xy2pct(x, y, z, circuit_short_name) to convert any x, y, and z(optional) to a percentage along the track you specify in circuit_short_name. to find the variable, use the openf1 docs: https://api.openf1.org/v1/meetings?year=2026&country_name=Singapore and replace the country name with the one you want.
