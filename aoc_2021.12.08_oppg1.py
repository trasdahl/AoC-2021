"""
Because the digits 1, 4, 7, and 8 each use a unique number of segments, you should be able to tell which combinations of signals correspond to those digits. Counting only digits in the output values (the part after | on each line), in the above example, there are 26 instances of digits that use a unique number of segments (highlighted above).

In the output values, how many times do digits 1, 4, 7, or 8 appear?
"""

import numpy as np
import pandas as pd

datafile = "Data/08_input.txt"
# datafile = "Data/08_input_test.txt"

num_1478 = 0
with open(datafile, 'r') as file:
    for i,line in enumerate(file):
        # print(line.strip())
        signal_patterns_str, output_values_str = [s.strip() for s in line.split('|')]
        # print(signal_patterns_str, output_values_str)
        output_values = output_values_str.split(' ')
        words_1478 = [s for s in output_values if len(s) in (2,3,4,7)]
        num_1478 += len(words_1478)
        print(f"{i:3d}) {output_values_str:30}. Relevante ord: {words_1478} (Løpende total: {num_1478:3d})")

print()
print("Antall av 1,4, eller 8:", num_1478)

