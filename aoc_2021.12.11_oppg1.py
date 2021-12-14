"""
The energy level of each octopus is a value between 0 and 9. Here, the top-left octopus has an energy level of 5, the bottom-right one has an energy level of 6, and so on.

You can model the energy levels and flashes of light in steps. During a single step, the following occurs:

First, the energy level of each octopus increases by 1.
Then, any octopus with an energy level greater than 9 flashes. This increases the energy level of all adjacent octopuses by 1, including octopuses that are diagonally adjacent. If this causes an octopus to have an energy level greater than 9, it also flashes. This process continues as long as new octopuses keep having their energy level increased beyond 9. (An octopus can only flash at most once per step.)
Finally, any octopus that flashed during this step has its energy level set to 0, as it used all of its energy to flash.
"""

import numpy as np
import pandas as pd
import scipy

datafile = "Data/11_input.txt"
# datafile = "Data/11_input_test.txt"
# datafile = "Data/11_input_minitest.txt"

with open(datafile, 'r') as file:
    n = len(file.readline().strip())
df = pd.read_fwf(datafile, widths=[1]*n, header=None, skiprows=0) # , columns='abcdefghijkl')
# x = df.values
x = np.zeros((df.shape[0]+2, df.shape[1]+2), dtype=int)
x[1:-1, 1:-1] = df.values
mask = np.zeros(x.shape, dtype=int)
mask[1:-1, 1:-1] = 1
print(x[1:-1, 1:-1])

tot_flashes = 0
for step in range(1, 101):
    x[1:-1, 1:-1] += 1
    # flash = x > 9
    # print(x[1:-1, 1:-1])
    to_flash = x == 10
    has_flashed = np.zeros(x.shape, dtype=bool)
    ivec,jvec = [list(i) for i in np.where(x == 10)]
    while len(ivec) > 0:
        iflash,jflash = ivec.pop(0), jvec.pop(0)
        for i in range(iflash-1, iflash+2):
            for j in range(jflash-1, jflash+2):
                if not (i == iflash and j == jflash):
                    x[i, j] += 1
                    x *= mask
                    if x[i, j] == 10:
                        ivec.append(i)
                        jvec.append(j)
        # x[i-1:i+2, j-1:j+2] += 1
        
        # print(x[1:-1, 1:-1])
        # ivec,jvec = np.where(x == 10)
        # for i,j in zip(ivec, jvec):
            # to_flash[i,j] = False
            # # print(i,j)
            # x[i-1:i+2, j-1:j+2] += 1
            
        # print(x)
    nflashes = (x > 9).sum()
    tot_flashes += nflashes
    x[x > 9] = 0
    print(f"After step {step} ({nflashes} flashes):")
    print(x[1:-1, 1:-1])

print(f"Total number of flashes: {tot_flashes}")