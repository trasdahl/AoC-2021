"""
--- Part Two ---
On the other hand, it might be wise to try a different strategy: let the giant squid win.

You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time counting its arms, the safe thing to do is to figure out which board will win last and choose that one. That way, no matter which boards it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after 13 is eventually called and its middle column is completely marked. If you were to keep playing until this point, the second board would have a sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score be?
"""

import numpy as np
import pandas as pd

datafile = "Data/04_input.txt"

# df_raw = pd.read_fwf(datafile, widths=[(0,1), (3,4), (6,7)], header=None, skiprows=2) # , columns='abcdefghijkl')
df_raw = pd.read_csv(datafile, delim_whitespace=True, header=None, skiprows=2) # , columns='abcdefghijkl')
df = df_raw.copy()
print("Antall tall lest inn   :", df.shape[0])
boards = df.values.reshape([100,5,5])
print(df.head(5))
print(boards[0,:,:])

# draw_numbers = pd.read_csv(datafile, delim_whitespace=True, header=None, skiprows=2) # , columns='abcdefghijkl')
with open(datafile) as file:
    draw_numbers = [int(s) for s in file.readline().split(',')]

print("Trekkerekkefølge:", draw_numbers)

ticks = np.zeros(boards.shape)

 
winners = []
for i, draw in enumerate(draw_numbers):
    print(f"{i+1:2d})", draw)
    ticks[boards == draw] = 1
    row_winners = np.where((ticks.sum(axis=1) == 5).any(axis=1))[0].tolist()
    col_winners = np.where((ticks.sum(axis=2) == 5).any(axis=1))[0].tolist()
    board_winners = list(set(row_winners + col_winners))
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
winner_board = boards[winner, :, :]
unmarked = winner_board * (1 - ticks[winner, :, :])
print(winner_board)
print("Umerkede tall:\n", unmarked)

print("Siste tall trukket:", draw)
print("Sum av åpne tall  :", unmarked.sum().sum())
print("Løsning           :", draw * unmarked.sum().sum())



