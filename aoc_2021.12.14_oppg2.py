"""
The first line is the polymer template - this is the starting point of the process.

The following section defines the pair insertion rules. A rule like AB -> C means that when elements A and B are immediately adjacent, element C should be inserted between them. These insertions all happen simultaneously.

So, starting with the polymer template NNCB, the first step simultaneously considers all three pairs:

The first pair (NN) matches the rule NN -> C, so element C is inserted between the first N and the second N.
The second pair (NC) matches the rule NC -> B, so element B is inserted between the N and the C.
The third pair (CB) matches the rule CB -> H, so element H is inserted between the C and the B.
Note that these pairs overlap: the second element of one pair is the first element of the next pair. Also, because all pairs are considered simultaneously, inserted elements are not considered to be part of a pair until the next step.
"""

import numpy as np
import pandas as pd
import scipy
import datetime
from collections import Counter

begin_time = datetime.datetime.now()

datafile = "Data/14_input.txt"
# datafile = "Data/14_input_test.txt"


def read_from_file(filename):
    pairdict = {}
    with open(filename, 'r') as file:
        polymer = file.readline().strip()
        file.readline() # Blank line
        insertions = []
        for line in file:
            insertions.append(line.strip().split(' -> '))
    unique_chars = sorted(set(polymer + ''.join([pair+new_char for pair,new_char in insertions])))
    paircount = {c1+c2:0 for c1 in unique_chars for c2 in unique_chars}
    for i in range(len(polymer) - 1):
        paircount[polymer[i:i+2]] += 1
    last_pair = polymer[-2:]
    return polymer, paircount, last_pair, dict(insertions)

def print_paircount(paircount):
    print("Pair count:", [(k,v) for k,v in paircount.items() if v > 0])

def letter_count(paircount, last_pair):
    letters = set(''.join(paircount.keys()))
    letter_count = dict.fromkeys(set(''.join(paircount.keys())), 0)
    for pair,count in paircount.items():
        letter_count[pair[0]] += count
    letter_count[last_pair[-1]] += 1
    return letter_count
        
def score(paircount, last_pair):
    lc = letter_count(paircount, last_pair)
    ls = sorted(lc, key=lc.get)
    return lc[ls[-1]] - lc[ls[0]] # , lc[ls[-1]], lc[ls[0]]

polymer, paircount, last_pair, insertions = read_from_file(datafile)
print("Template:     ", polymer)
print("Insertions:", insertions)
# print_paircount(paircount)
# print("Pair count:", paircount)


nsteps = 40
for step in range(1, nsteps+1):
    i = 0
    old_paircount = paircount.copy()
    for pair,new_char in insertions.items():
        new_pair1 = pair[0] + new_char
        new_pair2 = new_char + pair[1]
        paircount[new_pair1] += old_paircount[pair]
        paircount[new_pair2] += old_paircount[pair]
        paircount[pair] -= old_paircount[pair]
        if pair == last_pair:
            last_pair = new_char + pair[1]
    # print_paircount(paircount)
    # print(letter_count(paircount, last_pair))
    print(f"{step:2d}) Polymer length = {sum(paircount.values())+1:15d}, score = {score(paircount, last_pair):15d}")


print(f"Script runtime = {datetime.datetime.now() - begin_time}s")

