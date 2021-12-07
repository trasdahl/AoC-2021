"""
Initial state: 3,4,3,1,2
After  1 day:  2,3,2,0,1
After  2 days: 1,2,1,6,0,8
After  3 days: 0,1,0,5,6,7,8
After  4 days: 6,0,6,4,5,6,7,8,8
After  5 days: 5,6,5,3,4,5,6,7,7,8
After  6 days: 4,5,4,2,3,4,5,6,6,7
After  7 days: 3,4,3,1,2,3,4,5,5,6
After  8 days: 2,3,2,0,1,2,3,4,4,5
After  9 days: 1,2,1,6,0,1,2,3,3,4,8
After 10 days: 0,1,0,5,6,0,1,2,2,3,7,8
After 11 days: 6,0,6,4,5,6,0,1,1,2,6,7,8,8,8
After 12 days: 5,6,5,3,4,5,6,0,0,1,5,6,7,7,7,8,8
After 13 days: 4,5,4,2,3,4,5,6,6,0,4,5,6,6,6,7,7,8,8
After 14 days: 3,4,3,1,2,3,4,5,5,6,3,4,5,5,5,6,6,7,7,8
After 15 days: 2,3,2,0,1,2,3,4,4,5,2,3,4,4,4,5,5,6,6,7
After 16 days: 1,2,1,6,0,1,2,3,3,4,1,2,3,3,3,4,4,5,5,6,8
After 17 days: 0,1,0,5,6,0,1,2,2,3,0,1,2,2,2,3,3,4,4,5,7,8
After 18 days: 6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8
Each day, a 0 becomes a 6 and adds a new 8 to the end of the list, while each other number decreases by 1 if it was present at the start of the day.

In this example, after 18 days, there are a total of 26 fish. After 80 days, there would be a total of 5934.

Find a way to simulate lanternfish. How many lanternfish would there be after 80 days?
"""

import numpy as np
import pandas as pd

datafile = "Data/06_input.txt"

a = np.genfromtxt(datafile, delimiter=',', dtype=int)
print("Utgangspunkt:\n", a, "\n")

def tell_typer(a):
    unique, counts = np.unique(a, return_counts=True)
    x = np.zeros(9, dtype=int)
    x[unique] = counts
    # for i in range(len(unique)):
        # x[int(unique
    return x
    # return ", ".join([f"{int(unique[i])}:{counts[i]}" for i in range(len(unique))])
    # return np.vstack([unique, counts]).T

for day in range(1, 81):
    # print(tell_typer(a))
    a -= 1
    til_reset = a == -1
    ant_nye = len(a[til_reset])
    a[til_reset] = 6
    nye = 8 * np.ones(ant_nye, dtype=int)
    ant_gamle = len(a)
    a = np.concatenate([a, nye])
    print(f"Etter dag {day:2d}) {ant_gamle:7d} + {ant_nye:6d} = {len(a):7d} fisker (Fordeling: {tell_typer(a)})")
    # unique, counts = np.unique(a, return_counts=True)
    # print(f"Etter dag {day:2d}) {ant_gamle:7d} + {ant_nye:6d} = {len(a):7d} fisker (Fordeling: {counts})")
    # print(a)
