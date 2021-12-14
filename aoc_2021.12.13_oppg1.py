"""
Your goal is to find the number of distinct paths that start at start, end at end, and don't visit small caves more than once. There are two types of caves: big caves (written in uppercase, like A) and small caves (written in lowercase, like b). It would be a waste of time to visit any small cave more than once, but big caves are large enough that it might be worth visiting them multiple times. So, all paths you find should visit small caves at most once, and can visit big caves any number of times.
"""

import numpy as np
import pandas as pd
import scipy
import datetime

begin_time = datetime.datetime.now()

datafile = "Data/13_input.txt"
# datafile = "Data/13_input_test.txt"

def read_data(filename):
    x = []
    y = []
    folding_axes = []
    folding_coords = []
    with open(filename, 'r') as file:
        for line in file:
            # print(line.strip())
            if len(line.strip()) == 0:
                break
            thisx,thisy = [int(s) for s in line.strip().split(',')]
            x.append(thisx)
            y.append(thisy)
            
        for line in file:
            arr = line.strip().split(' ')
            axis,coord = arr[2].split('=')
            folding_axes.append(axis)
            folding_coords.append(int(coord))
    return x,y,folding_axes,folding_coords

def print_grid(grid, type=1):
    if type == 0:
        print(grid.astype(int).T)
    elif type == 1:
        for y in range(grid.shape[1]):
            s = ''.join(['.' if x == 0 else '#' for x in grid[:,y]])
            print(s)
            
def fold(grid, axis, coord):
    if axis == 'x':
        return grid[:coord, :] + grid[:grid.shape[0]-coord-1:-1, :]
    elif axis == 'y':
        return grid[:, :coord] + grid[:, :grid.shape[1]-coord-1:-1]

x,y,folding_axes,folding_coords = read_data(datafile)
grid = np.zeros((max(x)+1, max(y)+1), dtype=bool)
print(np.vstack((x,y)),'\nFolding:\n',folding_axes,folding_coords)
grid[x,y] = 1
if np.prod(grid.shape) < 300:
    print_grid(grid)


nfolds = len(folding_axes)
# nfolds = 1
solution_1 = 0
for fold_no, (axis,coord) in enumerate(zip(folding_axes[:nfolds],folding_coords[:nfolds]), start=1):
    grid = fold(grid, axis, coord)
    print(f"{fold_no:2}) Fold along {axis}={coord}. Number of dots:", grid.sum())
    if np.prod(grid.shape) < 300:
        print_grid(grid)
    if fold_no == 1:
        solution_1 = grid.sum()

print("\nSolution to part 1:", solution_1)

print(f"\nScript runtime = {datetime.datetime.now() - begin_time}s")

