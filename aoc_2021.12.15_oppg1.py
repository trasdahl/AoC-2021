"""
You start in the top left position, your destination is the bottom right position, and you cannot move diagonally. The number at each position is its risk level; to determine the total risk of an entire path, add up the risk levels of each position you enter (that is, don't count the risk level of your starting position unless you enter it; leaving it adds no risk to your total).

Your goal is to find a path with the lowest total risk. In this example, a path with the lowest total risk is highlighted here:

1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
The total risk of this path is 40 (the starting position is never entered, so its risk is not counted).
"""

import numpy as np
import pandas as pd
import scipy
import datetime
from collections import (defaultdict, deque)

begin_time = datetime.datetime.now()

datafile = "Data/15_input.txt"
datafile = "Data/15_input_test.txt"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def read_file(filename):
    with open(datafile, 'r') as file:
        n = len(file.readline().strip())
    df = pd.read_fwf(datafile, widths=[1]*n, header=None, skiprows=0)
    return df.values

def distance(i1, j1, i2, j2):
    return abs(i2-i1) + abs(j2-j1)

def cheapest_path(x, istart, jstart, iend, jend):
    # print(f"Cheapest path from ({istart}, {jstart}) to ({iend}, {jend}).")
    if distance(istart, jstart, iend, jend) == 1:
        path = [(istart, jstart)]
        score = 0
    elif iend == 0:
        path, score = cheapest_path(x, istart, jstart, iend, jend-1)
    elif jend == 0:
        path, score = cheapest_path(x, istart, jstart, iend-1, jend)
    else:
        path1, score1 = cheapest_path(x, istart, jstart, iend-1, jend)
        path2, score2 = cheapest_path(x, istart, jstart, iend, jend-1)
        path = path1 if score1 <= score2 else path2
        score = score1 if score1 <= score2 else score2
    return path + [(iend, jend)], score + x[iend, jend]

def cheapest_path2(x, istart, jstart, iend, jend):
    score = np.zeros((iend-istart+1, jend-jstart+1), dtype=int)
    path = [(istart,jstart)]
    for i in range(iend-istart+1):
        for j in range(jend-jstart+1):
            if i == 0 and j == 0:
                continue
            elif i == 0 and j > 0:
                score[i,j] = score[i, j-1] + x[i,j]
                # path = 
            elif i > 0 and j == 0:
                score[i,j] = score[i-1, j] + x[i,j]
            else:
                score[i,j] = min(score[i-1, j], score[i, j-1]) + x[i,j]
    return [], score

def cheapest_path3(x, istart, jstart, iend, jend, score):
    # score = np.zeros((iend-istart+1, jend-jstart+1), dtype=int)
    path = [(istart,jstart)]
    iwall, jwall = x.shape[0]-1, x.shape[1]-1 # Allowing for (iend, jend) not to be the lower right corner
    for i in range(iend-istart+1):
        for j in range(jend-jstart+1):
            if i == 0 and j == 0:
                continue
            elif i == 0:
                score[i,j] = score[i, j-1] + x[i,j]
            elif j == 0:
                score[i,j] = score[i-1, j] + x[i,j]
            elif i == iwall or j == jwall:
                score[i,j] = min(score[i-1, j], score[i, j-1]) + x[i,j]
            else:
                score[i,j] = min(score[i-1, j], score[i, j-1], score[i+1, j-1]+x[i+1,j], score[i-1, j+1]+x[i,j+1]) + x[i,j]
    return [], score

def cheapest_path4(x, istart, jstart, iend, jend, score):
    # score = np.zeros((iend-istart+1, jend-jstart+1), dtype=int)
    path = [(istart,jstart)]
    iwall, jwall = x.shape[0]-1, x.shape[1]-1 # Allowing for (iend, jend) not to be the lower right corner
    for i in range(iend-istart+1):
        for j in range(jend-jstart+1):
            if i == 0 and j == 0:
                continue
            score_left = score[i-1, j] if i > 0 else 999
            score_right = score[i+1, j] if i < iwall else 999
            score_up = score[i, j-1] if j > 0 else 999
            score_down = score[i, j+1] if j < jwall else 999
            score[i,j] = min(score_left, score_right, score_up, score_down) + x[i,j]
    return [], score

def print_path(grid, path=[]):
    s = f""
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if (i,j) in path:
                s += f"{bcolors.OKGREEN}{grid[i,j]}{bcolors.ENDC}"
            else:
                s += f"{grid[i,j]}"
        s += '\r\n'
    print(s)

x = read_file(datafile)
iend, jend = x.shape[0]-1, x.shape[1]-1
path, score = cheapest_path2(x, 0, 0, iend, jend)
highscore = score[-1,-1]
print("Total risk of chosen path:", highscore)
# We have to to optimize the path many times since it only allows one step
# local movement for each path point in each iteration.
for n in range(100):
    path, score = cheapest_path4(x, 0, 0, iend, jend, score)
    print("Total risk of chosen path:", highscore)
    if score[-1,-1] < highscore:
        highscore = score[-1,-1]
    else:
        pass
        # break
# print_path(x, path)


print(f"\nScript runtime = {datetime.datetime.now() - begin_time}s")

