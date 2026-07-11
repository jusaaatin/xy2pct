workflow:

1. use [generatelaparray.py](https://github.com/jusaaatin/f1-xy2pct/blob/main/generatelaparray.py) to spit out a file with x, y, and z coordinates for the track
2. manually delete extra data points and assign relevant ones to pit lane
3. use [parselaparray.py](https://github.com/jusaaatin/f1-xy2pct/blob/main/parselaparray.py) to check work (sample code to also go from file to array)
4. use [xy2pct.py](https://github.com/jusaaatin/f1-xy2pct/blob/main/xy2pct.py) to convert any coordinate to a percentage along the track
