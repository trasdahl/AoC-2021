"""
Each digit of a seven-segment display is rendered by turning on or off any of seven segments named a through g:

  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg


Because the digits 1, 4, 7, and 8 each use a unique number of segments, you should be able to tell which combinations of signals correspond to those digits. Counting only digits in the output values (the part after | on each line), in the above example, there are 26 instances of digits that use a unique number of segments (highlighted above).

In the output values, how many times do digits 1, 4, 7, or 8 appear?
"""

import numpy as np
import pandas as pd

datafile = "Data/08_input.txt"
# datafile = "Data/08_input_test.txt"

ss_digits = {'abcefg':0, 'cf':1, 'acdeg':2, 'acdfg':3, 'bcdf':4,
             'abdfg':5, 'abdefg':6, 'acf':7, 'abcdefg':8, 'abcdfg':9}

def letter_diff(str_a, str_b):
    diff_set = set(str_a) - set(str_b)
    assert len(diff_set) == 1, f"Diffen mellom {str_a} og {str_b} er IKKE én bokstav."
    return diff_set.pop()
    
def decode_word(word, letter_mapping):
    return ''.join(sorted([letter_mapping[letter] for letter in word]))


total = 0
with open(datafile, 'r') as file:
    for i,line in enumerate(file):
        # print(line.strip())
        signal_patterns_str, output_values_str = [s.strip() for s in line.split('|')]
        # print(signal_patterns_str, output_values_str)
        signals = signal_patterns_str.split(' ')
        output_values = output_values_str.split(' ')
        # len_count = {2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
        len_count = dict.fromkeys([2,3,4,5,6,7], 0)
        letter_count = dict.fromkeys('abcdefg', 0)
        letter_mapping = dict.fromkeys('abcdefg', '')
        str_1, str_4, str_7, str_8 = '', '', '', ''

        # Vi kan skille ut 1, 4, 7 og 8 på antall tegn: 1:2, 4:4, 7:3, 8:7 (0:6, 2:5, 3:5, 5:5, 6:6, 9:6)
        for s in signals:
            len_count[len(s)] += 1
            for letter in s:
                letter_count[letter] += 1
            if len(s) == 2:
                str_1 = s
            elif len(s) == 3:
                str_7 = s
            elif len(s) == 4:
                str_4 = s
            elif len(s) == 7:
                str_8 = s
        # print(sorted(letter_count.values()))
        
        # Seven segment display består av 7 segmenter, fra "a" til "g":
        #  aaaa 
        # b    c
        # b    c
        #  dddd 
        # e    f
        # e    f
        #  gggg 
        # Signal-delen av hver linje består av tallene 0-9, hver én gang. Vi vet ikke rekkefølgen.
        # Men vi vet at f.eks. segment a vil forekomme 8 ganger, segment b 6 ganger osv:
        # a:8, b:6, c:8, d:7, e:4, f:9, g:7: 
        # Basert på segment-telling kan vi identifisere b, e og f (siden de har et unikt antall forekomster).
        for letter, count in letter_count.items():
            if count == 4:
                letter_mapping['e'] = letter
            elif count == 6:
                letter_mapping['b'] = letter
            elif count == 9:
                letter_mapping['f'] = letter
        # Så kan vi finne ut c fra 1'eren
        letter_mapping['c'] = letter_diff(str_1, letter_mapping['f'])
        # Så finner vi a fra 7'eren
        letter_mapping['a'] = letter_diff(str_7, letter_mapping['c']+letter_mapping['f'])
        # Så finner vi d fra 4'eren
        letter_mapping['d'] = letter_diff(str_4, letter_mapping['b']+letter_mapping['c']+letter_mapping['f'])
        # Så finner vi g fra 8'eren
        letter_mapping['g'] = letter_diff(str_8, ''.join(letter_mapping.values()))

        # Ops, mappingen går motsatt vei av hva vi trenger.
        # Bare inverterer den her i stedet for å kode om (leve latskapen).
        letter_mapping = {value:key for (key,value) in letter_mapping.items()}
        # print(letter_mapping)

        # for word in signals:
            # digit = ss_digits[decode_word(word, letter_mapping)]
            # output += str(digit)
            # print(word, digit)
        
        output = ''
        for word in output_values:
            digit = ss_digits[decode_word(word, letter_mapping)]
            output += str(digit)
            # print(word, digit)
        total += int(output)
        print(f"{i:3d}) {output_values_str:30}: {output} (Total = {total:7d})")
        # g er 
        
print()
print("Summen av alle tall i output-seksjonene:", total)

