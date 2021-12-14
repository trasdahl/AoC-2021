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
import datetime

begin_time = datetime.datetime.now()

datafile = "Data/11_input.txt"
# datafile = "Data/11_input_test.txt"
# datafile = "Data/11_input_minitest.txt"

with open(datafile, 'r') as file:
    n = len(file.readline().strip())
df = pd.read_fwf(datafile, widths=[1]*n, header=None, skiprows=0) # , columns='abcdefghijkl')
x = df.values
imax,jmax = x.shape
# x = np.zeros((df.shape[0]+2, df.shape[1]+2), dtype=int)
# x[1:-1, 1:-1] = df.values
# mask = np.zeros(x.shape, dtype=int)
# mask[1:-1, 1:-1] = 1
print("Before any steps:\n", x)

tot_flashes = 0
for step in range(1, 1000):
    x += 1
    has_flashed = x == 10
    i_to_flash,j_to_flash = [list(i) for i in np.where(x == 10)]
    # n = 0
    while len(i_to_flash) > 0:
        iflash,jflash = i_to_flash.pop(0), j_to_flash.pop(0)
        has_flashed[iflash, jflash] = True
        # print(f"Flashing ({iflash}, {jflash})")
        x[max(0,iflash-1):min(imax,iflash+2), max(0,jflash-1):min(jmax,jflash+2)] += 1
        i_new_flashes,j_new_flashes = np.where((x == 10) & (has_flashed == False))
        has_flashed[i_new_flashes,j_new_flashes] = True
        i_to_flash.extend(i_new_flashes) #  + iflash + 1)
        j_to_flash.extend(j_new_flashes) #  + jflash + 1)
        # print(f"Adding [{i_new_flashes}, {j_new_flashes}] to new flashes")
        # n += 1
        # if n == 50:
            # break
    nflashes = (x > 9).sum()
    tot_flashes += nflashes
    x[x > 9] = 0
    # print(f"After step {step} ({nflashes} flashes):")
    # print(x)
    if nflashes == mask.sum():
        print(f"Full synchronizity achieved at step {step}! All octopuses flashing.")
        break

print(f"Total number of flashes: {tot_flashes}")

print(f"Script runtime = {datetime.datetime.now() - begin_time}s")

