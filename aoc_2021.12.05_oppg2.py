"""
--- Part Two ---
Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture; you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your list will only ever be horizontal, vertical, or a diagonal line at exactly 45 degrees. In other words:

An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
Considering all lines from the above example would now produce the following diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....
You still need to determine the number of points where at least two lines overlap. In the above example, this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?
"""


import numpy as np
import pandas as pd

datafile = "Data/05_input.txt"

grid = pd.DataFrame(0, index=range(1000), columns=range(1000))

with open(datafile, 'r') as file:
    for i,line in enumerate(file):
        p1,p2 = line.split(' -> ')
        x1,y1 = [int(s) for s in p1.split(',')]
        x2,y2 = [int(s) for s in p2.split(',')]
        # x1,y1,x2,y2 = [s.split(',') for s in line.split(' -> ')]
        if x1 == x2 or y1 == y2:
            print(f"Horizontal or vertical line from ({x1}, {y1}) to ({x2}, {y2})")
            grid.loc[min(x1,x2):max(x1,x2), min(y1,y2):max(y1,y2)] += 1
        else:
            print(f"Diagonal line from ({x1}, {y1}) to ({x2}, {y2})")
            for i in range(max(x1,x2)- min(x1,x2) + 1):
                # print(x1 + np.sign(x2-x1)*i, y1 + np.sign(y2-y1)*i)
                grid.loc[x1 + np.sign(x2-x1)*i, y1 + np.sign(y2-y1)*i] +=1
        

s = grid.unstack().value_counts()
print("Value counts:\n", s)
print("Solution:", s[2:].sum())




