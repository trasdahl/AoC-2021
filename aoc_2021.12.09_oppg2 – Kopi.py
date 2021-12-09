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
# datafile = "Data/09_input_test2.txt"

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

minima = a.copy()
# Filtrer ut alt annet enn rand og minima
minima[1:-1, 1:-1][~(nedover & oppover & hoyre & venstre)] = -1
xmin_vec, ymin_vec =  np.where((-1 < minima) & (minima < 10))
minima_vec = a[xmin_vec, ymin_vec]
print(minima)
print()
for i in range(len(xmin_vec)):
    print(f"{i}) Minimum {minima_vec[i]} i punkt ({xmin_vec[i]:2d}, {ymin_vec[i]:2d})")

x_end = minima.shape[0]
y_end = minima.shape[1]
basin_sizes = np.zeros(len(xmin_vec), dtype=int)
for point_no, (xmin,ymin) in enumerate(zip(xmin_vec, ymin_vec)):
    minimum = a[xmin, ymin]
    basin = 10 * np.ones((df.shape[0] + 2, df.shape[1] + 2), dtype=int)
    basin[1:-1, 1:-1] = 0
    basin = np.zeros((df.shape[0] + 2, df.shape[1] + 2), dtype=int)
    basin[xmin, ymin] = 1

    print()
    print(a)
    print(f"{point_no}) Bassenget til minimum {minimum} i punkt ({xmin}, {ymin})")
    distances = range(1, 7)
    for dist in distances:
        points_considered = dict.fromkeys(distances, 0)
        points_added = dict.fromkeys(distances, 0)
        for x in range(max(xmin-dist, 0), min(xmin+dist+1, x_end)):
            for y in range(max(ymin-dist, 0), min(ymin+dist+1, y_end)):
                if np.abs(x-xmin) + np.abs(y-ymin) == dist:
                    points_considered[dist] += 1
                    print(f"Til vurdering i avstand {dist} fra ({xmin}, {ymin}): ({x}, {y})={a[x,y]}")
                    xsign = np.sign(xmin - x) # Direction towards minimum
                    ysign = np.sign(ymin - y) # Direction towards minimum
                    if a[x,y] < 9 and (basin[x + xsign, y] == 1 and a[x,y] >= a[x + xsign, y]
                                        or basin[x, y + ysign] == 1 and a[x,y] >= a[x, y + ysign]):
                        basin[x,y] = 1
                        print(f"Legger til a[{x}, {y}] = {a[x,y]} i avstand {dist} fra ({xmin}, {ymin}).")
                        points_added[dist] += 1
                        
        print(f"Avstand {dist}: {points_considered[dist]} evaluert, {points_added[dist]} lagt til.")
        if points_added[dist] == 0:
            break
    print("Basseng:")
    print(a * basin)
    print("Størrelse på bassenget:", basin.sum())
    basin_sizes[point_no] = basin.sum()

print()
for i in range(len(xmin_vec)):
    print(f"Bassenget til minimum {minima_vec[i]} i punkt ({xmin_vec[i]:2d}, {ymin_vec[i]:2d}): {basin_sizes[i]:4d}")

print("Løsning:", np.prod(np.sort(basin_sizes)[-3:])) # 449 550 er for lavt
