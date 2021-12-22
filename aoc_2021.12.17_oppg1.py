"""
The probe launcher on your submarine can fire the probe with any integer velocity in the x (forward) and y (upward, or downward if negative) directions. For example, an initial x,y velocity like 0,10 would fire the probe straight up, while an initial velocity like 10,-1 would fire the probe forward at a slight downward angle.

The probe's x,y position starts at 0,0. Then, it will follow some trajectory by moving in steps. On each step, these changes occur in the following order:

The probe's x position increases by its x velocity.
The probe's y position increases by its y velocity.
Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
Due to gravity, the probe's y velocity decreases by 1.
For the probe to successfully make it into the trench, the probe must be on some trajectory that causes it to be within a target area after any step. The submarine computer has already calculated this target area (your puzzle input). For example:

target area: x=20..30, y=-10..-5
This target area means that you need to find initial x,y velocity values such that after any step, the probe's x position is at least 20 and at most 30, and the probe's y position is at least -10 and at most -5.
"""

import numpy as np
import pandas as pd
import scipy
import datetime
from collections import (defaultdict, deque)

begin_time = datetime.datetime.now()

# target area: x=277..318, y=-92..-53
target = [277,318, -92,-53]
# target = [20, 30, -10, -5]
x0,x1,y0,y1 = target

def throw(x_init, y_init, tmax=10):
    # u = x-speed, v = y-speed
    # u = list(range(x_init, 0, -np.sign(x_init)))
    # u = u + [0] * (tmax - len(u) - 1)
    # v = list(range(y_init, y_init-tmax, -1))
    u = np.concatenate(([0], np.linspace(x_init, x_init-tmax+1, tmax, dtype=int)))
    u[u < 0] = 0
    v = np.concatenate(([0], np.linspace(y_init, y_init-tmax+1, tmax, dtype=int)))
    # print(u.tolist(), v.tolist())
    x, y = np.cumsum(u), np.cumsum(v)
    return x, y
    
def crop_after_target(x, y, target):
    # i, j = np.where(x <= x1)[0][-1], np.where(y >= y0)[0][-1]
    # last_idx = max(i,j)
    if target_hit(x, y, target):
        last_idx = first_step_within_target(x, y, target)
    else:
        last_idx = first_step_after_target(x, y, target)
        # return x[:last_idx+1], y[:last_idx+1]
    print(f"Cropping throw from {len(x)} steps to {last_idx} steps")
    return x[:last_idx+1], y[:last_idx+1]
        # return x[:np.where(x <= x1)[0][-1]+1], y[:np.where(y >= y0)[0][-1]+1]

def target_hit(x, y, target):
    return path_within_target(x, y, target).any()

def target_hit_vertically(x, y, target):
    return path_within_target(np.array([target[0]]), y, target).any()

def path_within_target(x, y, target):
    x0,x1,y0,y1 = target
    return (x0 <= x) & (x <= x1) & (y0 <= y) & (y <= y1)

def path_past_target(x, y, target):
    x0,x1,y0,y1 = target
    return (x >= x1) | (y <= y0)
    
def first_step_within_target(x, y, target):
    try:
        return np.where(path_within_target(x, y, target))[0][0]
    except IndexError:
        return []
    
def first_step_after_target(x, y, target):
    try:
        return np.where(path_past_target(x, y, target))[0][0]
    except IndexError:
        return []

def trajectory_highpoint(x, y):
    return y.max()
    
def draw_throw(x, y, target):
    x0,x1,y0,y1 = target
    xmin = min(x.min(), x0, x1)
    xmax = max(x.max(), x0, x1)
    ymin = min(y.min(), y0, y1)
    ymax = max(y.max(), y0, y1)
    # print(xmin, xmax, ymin, ymax)
    xy = list(zip(x, y))
    for j in range(ymax, ymin-2, -1):
        s = ''
        for i in range(xmin, xmax + 5):
            if i == x[0] and j == y[0]:
                s += 'S'
            elif (i,j) in xy:
                s += '#'
            elif x0 <= i <= x1 and y0 <= j <= y1:
                s += 'T'
            else:
                s += '.'
        print(s)
        

x_init, y_init = 24,3
tmax = 20
x, y = throw(x_init, y_init, tmax)
print(f"Hitting target? {target_hit(x, y, target)}")
x, y = crop_after_target(x, y, target)
# print(x, y)
# draw_throw(x, y, target)


y_rec = 0
for y_init in range(100):
    x, y = throw(x_init, y_init, 1000)
    if target_hit_vertically(x, y, target):
        y_rec = y.max()
    print(f"y_init={y_init}. Hitting target? {target_hit_vertically(x, y, target)}. Highpoint = {y.max()}")

print()
print("Highest shot that hits target:", y_rec)

print(f"\nScript runtime = {datetime.datetime.now() - begin_time}s")

