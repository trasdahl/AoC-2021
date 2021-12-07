"""
--- Day 4: Giant Squid ---
You're already almost 1.5km (almost a mile) below the surface of the ocean, already so deep that you can't see any sunlight. What you can see, however, is a giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. Numbers are chosen at random, and the chosen number is marked on all boards on which it appears. (Numbers may not appear on all boards.) If all numbers in any row or any column of a board are marked, that board wins. (Diagonals don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass the time. It automatically generates a random order in which to draw numbers and a random set of boards (your puzzle input). For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no winners, but the boards are marked as follows (shown here adjacent to each other to save space):

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still no winners:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
Finally, 24 is drawn:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
At this point, the third board wins because it has at least one complete row or column of marked numbers (in this case, the entire top row is marked: 14 21 17 24 4).

The score of the winning board can now be calculated. Start by finding the sum of all unmarked numbers on that board; in this case, the sum is 188. Then, multiply that sum by the number that was just called when the board won, 24, to get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win first. What will your final score be if you choose that board?
"""

import numpy as np
import pandas as pd

datafile = "C:/Users/D7Y/Documents/Jobb/Python/Advent of code/Data/04_input.txt"

# df_raw = pd.read_fwf(datafile, widths=[(0,1), (3,4), (6,7)], header=None, skiprows=2) # , columns='abcdefghijkl')
df_raw = pd.read_csv(datafile, delim_whitespace=True, header=None, skiprows=2) # , columns='abcdefghijkl')
df = df_raw.copy()
print("Antall tall lest inn   :", df.shape[0])
print(df.head(10))
print()


# draw_numbers = pd.read_csv(datafile, delim_whitespace=True, header=None, skiprows=2) # , columns='abcdefghijkl')
with open(datafile) as file:
    draw_numbers = [int(s) for s in file.readline().split(',')]
    
print("Trekkerekkefølge:", draw_numbers)

ticks = pd.DataFrame(0, index=df.index, columns=df.columns)
# print(ticks.shape)


def row_to_board_num(rows):
    return [int(n / 5) for n in rows]


def check_for_row_winners(ticks):
    row_winners = ticks[ticks.sum(axis=1) == 5].index.to_list()
    return row_winners # row_to_board_num(row_winners)
    
def check_for_col_winners(ticks):
    r5 = ticks.rolling(5).sum().max(axis=1) # Rad-max av R5 => høyeste R5 blant de fem kolonnene. 
    five_consecutive = r5[r5 == 5] # Begrens til de som har fem på rad. Men dette kan være på tvers av to brett.
    # col_winners = five_consecutive[five_consecutive.index % 5 == 0].index
    col_winners = (five_consecutive[five_consecutive.index % 5 == 4].index - 4).to_list()
    # col_winners = five_consecutive[five_consecutive.index.intersection(np.arange(5, len(ticks), 5))]
    return col_winners


for i, draw in enumerate(draw_numbers):
    print(f"{i+1:2d})", draw)
    ticks[df == draw] = 1
    row_winners = check_for_row_winners(ticks)
    col_winners = check_for_col_winners(ticks)
    # print(winners)
    if len(row_winners) > 0 or len(col_winners) > 0:
        winner = (row_winners + col_winners)[0]
        print("Vinner:", winner)
        break
    

winner_board = df.loc[winner:winner+4, :]
print(winner_board)
unmarked = winner_board * (1 - ticks.loc[winner:winner+4, :])
print(unmarked)

print("Siste tall trukket:", draw)
print("Sum av åpne tall  :", unmarked.sum().sum())
print("Løsning           :", draw * unmarked.sum().sum())



