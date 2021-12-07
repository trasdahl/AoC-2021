"""
--- Part Two ---
Next, you should verify the life support rating, which can be determined by multiplying the oxygen generator rating by the CO2 scrubber rating.

Both the oxygen generator rating and the CO2 scrubber rating are values that can be found in your diagnostic report - finding them is the tricky part. Both values are located using a similar process that involves filtering out values until only one remains. Before searching for either rating value, start with the full list of binary numbers from your diagnostic report and consider just the first bit of those numbers. Then:

Keep only numbers selected by the bit criteria for the type of rating value for which you are searching. Discard numbers which do not match the bit criteria.
If you only have one number left, stop; this is the rating value for which you are searching.
Otherwise, repeat the process, considering the next bit to the right.
The bit criteria depends on which type of rating value you want to find:

To find oxygen generator rating, determine the most common value (0 or 1) in the current bit position, and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 1 in the position being considered.
To find CO2 scrubber rating, determine the least common value (0 or 1) in the current bit position, and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 0 in the position being considered.
For example, to determine the oxygen generator rating value using the same example diagnostic report from above:

Start with all 12 numbers and consider only the first bit of each number. There are more 1 bits (7) than 0 bits (5), so keep only the 7 numbers with a 1 in the first position: 11110, 10110, 10111, 10101, 11100, 10000, and 11001.
Then, consider the second bit of the 7 remaining numbers: there are more 0 bits (4) than 1 bits (3), so keep only the 4 numbers with a 0 in the second position: 10110, 10111, 10101, and 10000.
In the third position, three of the four numbers have a 1, so keep those three: 10110, 10111, and 10101.
In the fourth position, two of the three numbers have a 1, so keep those two: 10110 and 10111.
In the fifth position, there are an equal number of 0 bits and 1 bits (one each). So, to find the oxygen generator rating, keep the number with a 1 in that position: 10111.
As there is only one number left, stop; the oxygen generator rating is 10111, or 23 in decimal.
Then, to determine the CO2 scrubber rating value from the same example above:

Start again with all 12 numbers and consider only the first bit of each number. There are fewer 0 bits (5) than 1 bits (7), so keep only the 5 numbers with a 0 in the first position: 00100, 01111, 00111, 00010, and 01010.
Then, consider the second bit of the 5 remaining numbers: there are fewer 1 bits (2) than 0 bits (3), so keep only the 2 numbers with a 1 in the second position: 01111 and 01010.
In the third position, there are an equal number of 0 bits and 1 bits (one each). So, to find the CO2 scrubber rating, keep the number with a 0 in that position: 01010.
As there is only one number left, stop; the CO2 scrubber rating is 01010, or 10 in decimal.
Finally, to find the life support rating, multiply the oxygen generator rating (23) by the CO2 scrubber rating (10) to get 230.

Use the binary numbers in your diagnostic report to calculate the oxygen generator rating and CO2 scrubber rating, then multiply them together. What is the life support rating of the submarine? (Be sure to represent your answer in decimal, not binary.)
"""

import numpy as np
import pandas as pd

datafile = "Data/03_input.txt"

df_raw = pd.read_fwf(datafile, widths=[1]*12, header=None) # , columns='abcdefghijkl')
df = df_raw.copy()
print("Antall tall lest inn   :", df.shape[0])
print(df.head())
print()

flertallskrav = len(df_raw) / 2
ant_enere = df.sum()
vanligst = (ant_enere > flertallskrav).astype(int)
sjeldnest = 1 - vanligst
toer_potens = pd.Series([2]*12).pow(vanligst.index[::-1])
print("Antall 1'ere per kolonne:")
print(pd.concat([ant_enere, vanligst, toer_potens, vanligst * toer_potens], axis=1))
print()



def filtrer_flertallskrav(df, col):
    # Større enn ELLER LIK gjør at vi velger 1 hvis det er uavgjort
    flertallskrav = len(df) / 2 # Odde lengde => rundes ned. OK, siden vi aldri får 50/50 ved odde lengde.
    vanligst = (df[col].sum() >= flertallskrav).astype(int)
    ant = (df[col] == vanligst).sum()
    print(f"Vanligst i posisjon {col:2d}: {vanligst} ({ant} av {len(df)})")
    return df[df[col] == vanligst]

for col in range(df_raw.shape[1]):
    df = filtrer_flertallskrav(df, col)
    # print(df.shape)
    # print(df.head(3))
    if len(df) == 1:
        break
        
oxygen = (df.iloc[0,:] * toer_potens).sum()
print("Oxygen generator code  :", ''.join([str(n) for n in df.iloc[0,:]]))
print("Oxygen generator rating:", (df.iloc[0,:] * toer_potens).sum())
print()



def filtrer_mindretallskrav(df, col):
    # Større enn ELLER LIK gjør at vi velger 1 hvis det er uavgjort
    flertallskrav = len(df) / 2 # Odde lengde => rundes ned. OK, siden vi aldri får 50/50 ved odde lengde.
    sjeldnest = (df[col].sum() < flertallskrav).astype(int)
    ant = (df[col] == sjeldnest).sum()
    # print(f"Sjeldnest i posisjon {col:2d}: {sjeldnest} ({ant} av {len(df)})")
    print(f"Posisjon {col:2d}: # {sjeldnest} : {ant:3d}, # {1-sjeldnest} : {len(df)-ant:3d} (Tot: {len(df)})")
    return df[df[col] == sjeldnest]


df = df_raw.copy()
for col in range(df_raw.shape[1]):
    df = filtrer_mindretallskrav(df, col)
    # print(df.shape)
    # print(df.head(3))
    if len(df) == 1:
        break
        
co2 = (df.iloc[0,:] * toer_potens).sum()
print("CO2 scrubber code  :", ''.join([str(n) for n in df.iloc[0,:]]))
print("CO2 scrubber rating:", (df.iloc[0,:] * toer_potens).sum())
print()


# print("Epsilon rate:", epsilon_rate)
print("Solution    :", oxygen * co2)



