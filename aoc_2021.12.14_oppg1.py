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
    with open(filename, 'r') as file:
        polymer = file.readline().strip()
        file.readline() # Blank line
        insertions = []
        for line in file:
            insertions.append(line.strip().split(' -> '))
    return polymer, dict(insertions)

polymer, insertions = read_from_file(datafile)
# pairs,elements = zip(*insertions)
print("Template:     ", polymer)
# print("Insertions:", insertions)
# print("Pairs:", pairs)
# print("Elements:", elements)

nsteps = 10
for step in range(1, nsteps+1):
    i = 0
    for n in range(len(polymer) - 1):
        pair = polymer[i:i+2]
        if pair in insertions.keys():
            polymer = polymer[:i+1] + insertions[pair] + polymer[i+1:]
            i += 2
        else:
            i += 1
    # print(f"After step {step}: ", polymer)
    letter_count = {c : polymer.count(c) for c in set(polymer)}
    letters_sorted = sorted(letter_count, key=letter_count.get)
    print(f"{step:2d}) Letter count: {letter_count} (Total={sum(letter_count.values())}). "
            f"Largest minus smallest = {letter_count[letters_sorted[-1]]-letter_count[letters_sorted[0]]}")

print(f"Script runtime = {datetime.datetime.now() - begin_time}s")

