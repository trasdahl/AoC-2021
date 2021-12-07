"""
--- Part Two ---
On the other hand, it might be wise to try a different strategy: let the giant squid win.

You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time counting its arms, the safe thing to do is to figure out which board will win last and choose that one. That way, no matter which boards it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after 13 is eventually called and its middle column is completely marked. If you were to keep playing until this point, the second board would have a sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score be?
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
num_boards = len(df) / 5

# draw_numbers = pd.read_csv(datafile, delim_whitespace=True, header=None, skiprows=2) # , columns='abcdefghijkl')
with open(datafile) as file:
    draw_numbers = [int(s) for s in file.readline().split(',')]
    
print("Trekkerekkefølge:", draw_numbers)

ticks = pd.DataFrame(0, index=df.index, columns=df.columns)
# print(ticks.shape)


def row_to_board_num(rows):
    return [int(n / 5) for n in rows]

def board_num_to_first_row(rows):
    return [5 * n for n in rows]

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


winners = []
for i, draw in enumerate(draw_numbers):
    print(f"{i+1:2d})", draw)
    ticks[df == draw] = 1
    row_winners = check_for_row_winners(ticks)
    col_winners = check_for_col_winners(ticks)
    board_winners = list(set(row_to_board_num(row_winners + col_winners)))
    new_winners = list(set(board_winners) - set(winners))
    print("New winners:", new_winners)
    winners += new_winners
    if len(winners) == num_boards:
        break
    # if len(new_winners) > 0:
        # winner = (row_winners + col_winners)[0]
        # print("Vinner:", winners)
        # for winner in winners:
            # df.drop(winner:winner+4, inplace=True)
    

last_winner = winners[-1]
print("Siste vinner:", last_winner)
winner = last_winner
winner_board = df.loc[5*winner:5*winner+4, :]
print(winner_board)
unmarked = winner_board * (1 - ticks.loc[5*winner:5*winner+4, :])
print(unmarked)

print("Siste tall trukket:", draw)
print("Sum av åpne tall  :", unmarked.sum().sum())
print("Løsning           :", draw * unmarked.sum().sum())



