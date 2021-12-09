"""
Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678
Each number corresponds to the height of a particular location, where 9 is the highest and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than any of its adjacent locations. Most locations have four adjacent locations (up, down, left, and right); locations on the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal locations do not count as adjacent.)

In the above example, there are four low points, all highlighted: two are in the first row (a 1 and a 0), one is in the third row (a 5), and one is in the bottom row (also a 5). All other locations on the heightmap have some lower adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, the risk levels of the low points are 2, 1, 6, and 6. The sum of the risk levels of all low points in the heightmap is therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk levels of all low points on your heightmap?
"""

import numpy as np
import pandas as pd
import scipy

datafile = "Data/09_input.txt"
# datafile = "Data/09_input_test.txt"

with open(datafile, 'r') as file:
    n = len(file.readline().strip())
df = pd.read_fwf(datafile, widths=[1]*n, header=None, skiprows=0) # , columns='abcdefghijkl')
print(df.shape)
print(df)

# Plasser matrisen inni en ramme av større tall så du slipper å sjekke randbetingelsen
a = 10 * np.ones((df.shape[0] + 2, df.shape[1] + 2), dtype=int)
a[1:-1, 1:-1] = df.values
print(a)

# Sammenlign alle tall med naboene i alle retninger
nedover = a[1:-1, 1:-1] - a[2:, 1:-1] < 0 
oppover = a[1:-1, 1:-1] - a[:-2, 1:-1] < 0
hoyre   = a[1:-1, 1:-1] - a[1:-1, 2:] < 0 
venstre = a[1:-1, 1:-1] - a[1:-1, :-2] < 0 
print("Lokale minima:", a[1:-1, 1:-1][nedover & oppover & hoyre & venstre])
print("Solution:", (a[1:-1, 1:-1][nedover & oppover & hoyre & venstre] + 1).sum())

# print(scipy.signal.argrelextrema(df.values, np.less))
# print(df.values[scipy.signal.argrelextrema(df.values, np.less)])


