"""
The probe launcher on your submarine can fire the probe with any integer velocity in the x (forward) and y (upward, or downward if negative) directions. For example, an initial x,y velocity like 0,10 would fire the probe straight up, while an initial velocity like 10,-1 would fire the probe forward at a slight downward angle.

The probe's x,y position starts at 0,0. Then, it will follow some trajectory by moving in steps. On each step, these changes occur in the following order:

The probe's x position increases by its x velocity.
The probe's y position increases by its y velocity.
Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
Due to gravity, the probe's y velocity decreases by 1.
For the probe to successfully make it into the trench, the probe must be on some trajectory that causes it to be within a target area after any step. The submarine computer has already calculated this target area (your puzzle input). For example:

target area: x=20..30, y=-10..-5
This target area means that you need to find initial x,y velocity values such that after any step, the probe's x position is at least 20 and at most 30, and the probe's y position is at least -10 and at most -5.
"""

import numpy as np
import pandas as pd
import scipy
import datetime
from collections import (defaultdict, deque)
import math

begin_time = datetime.datetime.now()
DEBUG = False

class SnailfishNumber():
    """
    Version where each SnailfishNumber is recursively built up of left and right SnailfishNumbers
    """
    def __init__(self, left=None, right=None, verbose=False): # or default to [] ?
        self.left = left
        self.right = right
        # self.reduce()
        
    def __str__(self):
        return f"[{self.left.__str__()},{self.right.__str__()}]"

    def __add__(self, other):
        # if len(self.l) == 0: # Definition of zero: self.l = []
        if self.left is None and self.right is None: # Definition of zero: [None, None]
            return other
        elif other.left is None and other.right is None: # Definition of zero: [None, None]
            return self
        else:
            return SnailfishNumber(self, other).reduce()
        
    def __radd__(self, other):
        # if len(self.l) == 0: # Definition of zero: self.l = []
        if self.left is None and self.right is None: # Definition of zero: [None, None]
            return other
        elif other.left is None and other.right is None: # Definition of zero: [None, None]
            return self
        else:
            return SnailfishNumber(other, self).reduce()
        
    def __abs__(self):
        return 3 * abs(self.left) + 2 * abs(self.right)

    def find_bugs(self):
        return

    def left_depth(self):
        return self.left.max_depth() if isinstance(self.left, SnailfishNumber) else 0

    def right_depth(self):
        return self.right.max_depth() if isinstance(self.right, SnailfishNumber) else 0

    def max_depth(self):
        left_depth = self.left.max_depth() if isinstance(self.left, SnailfishNumber) else 0
        right_depth = self.right.max_depth() if isinstance(self.right, SnailfishNumber) else 0
        # return max(1 + self.left.max_depth(), 1 + self.right.max_depth())
        return 1 + max(left_depth, right_depth)

    def reduce(self):
        if self.left is None and self.right is None:
            return
        else:
            finished = False
            if DEBUG:
                print("Before reduction:", self)
            for i in range(10000):
                rest_l, rest_r, explosions = self.explode()
                if explosions == 0:
                    splits = self.split()
                    if explosions == 0 and splits == 0:
                        break
        # if self.left_depth() >= 4:
        # self.explode()
        # if self.left_depth() == 0 and abs(self.left) > 9:
            # self.left = SnailfishNumber(math.floor(self.left / 2), math.ceil(self.left / 2))
        # if self.right_depth() == 0 and abs(self.right) > 9:
            # self.right = SnailfishNumber(math.floor(self.right / 2), math.ceil(self.right / 2))
        # self.find_bugs()
        # while len(self.bugs) > 0:
            # bug = self.bugs.pop(0)
            # if bug['type'] == 'explode':
                # self.explode()
            # elif bug['type'] == 'split':
                # self.split()
        return self
    
    def explode(self, depth=0, explosions=0, max_explosions=1):
        # print(self, depth, explosions, max_explosions)
        rest_l, rest_r = 0,0
        if depth >= 3 and self.max_depth() == 2: # Denne bør være ett nivå over dypeste nivå.
            s_pre = str(self)
            if isinstance(self.left, SnailfishNumber) and explosions < max_explosions:
                if isinstance(self.right, SnailfishNumber):
                    self.right.add_leftmost(self.left.right)
                else: # self.right should be int here
                    self.right += self.left.right
                rest_l = self.left.left
                self.left = 0
                explosions += 1
                if DEBUG:
                    print("Explosion!", s_pre, "became", str(self))
            if isinstance(self.right, SnailfishNumber) and explosions < max_explosions:
                if isinstance(self.left, SnailfishNumber):
                    self.left.add_rightmost(self.right.left)
                else: # self.left should be int here
                    self.left += self.right.left
                rest_r = self.right.right
                self.right = 0
                explosions += 1
                if DEBUG:
                    print("Explosion!", s_pre, "became", str(self))
        else:
            if isinstance(self.left, SnailfishNumber) and explosions < max_explosions:
                # self.left += self.left.explode(depth+1)
                rest_l,rest_r,explosions = self.left.explode(depth+1, explosions, max_explosions)
                if isinstance(rest_r, SnailfishNumber) or rest_r > 0:
                    if isinstance(self.right, SnailfishNumber):
                        self.right.add_leftmost(rest_r)
                        rest_r = 0
                    elif isinstance(self.right, int):
                        if DEBUG:
                            print("Adding rest_r", rest_r, "to right=", self.right, "at depth", depth)
                        self.right += rest_r
                        rest_r = 0
            if isinstance(self.right, SnailfishNumber) and explosions < max_explosions:
                # self.right += self.right.explode(depth+1)
                rest_l,rest_r,explosions = self.right.explode(depth+1, explosions, max_explosions)
                if isinstance(rest_l, SnailfishNumber) or rest_l > 0:
                    if isinstance(self.left, SnailfishNumber):
                        self.left.add_rightmost(rest_l)
                        rest_l = 0
                    elif isinstance(self.left, int):
                        if DEBUG:
                            print("Adding rest_r", rest_l, "to left=", self.left, "at depth", depth)
                        self.left += rest_l
                        rest_l = 0
        # self.add_rest(rest_l, rest_r)
        # self.right += self.left.right
        # self.left = 0
        # print("Rest", (rest_l,rest_r), "at depth", depth)
        if depth == 0 and explosions > 0 and DEBUG:
            print("After explosion:", self)
        return rest_l, rest_r, explosions
    
    def add_leftmost(self, scalar):
        if scalar == 0:
            return
        elif isinstance(self.left, SnailfishNumber):
            self.left.add_leftmost(scalar)
        elif isinstance(self.left, int):
            self.left += scalar

    def add_rightmost(self, scalar):
        if scalar == 0:
            return
        elif isinstance(self.right, SnailfishNumber):
            self.right.add_rightmost(scalar)
        elif isinstance(self.right, int):
            self.right += scalar

    def split(self, depth=0, splits=0, max_splits=1):
        if splits >= max_splits:
            return splits
        if isinstance(self.left, int):
            if abs(self.left) > 9 and splits < max_splits:
                if DEBUG:
                    print("Found", self.left, "at depth", depth, ". Splitting")
                splits += 1
                self.left = SnailfishNumber(math.floor(self.left / 2), math.ceil(self.left / 2))
                # print("After split:", self)
        elif isinstance(self.left, SnailfishNumber) and splits < max_splits:
            splits = self.left.split(depth+1)
        if isinstance(self.right, int) and splits < max_splits:
            if abs(self.right) > 9:
                if DEBUG:
                    print("Found", self.right, "at depth", depth, ". Splitting")
                splits += 1
                self.right = SnailfishNumber(math.floor(self.right / 2), math.ceil(self.right / 2))
        elif isinstance(self.right, SnailfishNumber) and splits < max_splits:
            splits = self.right.split(depth+1)
        if depth == 0 and splits > 0 and DEBUG:
            print("After split:", self, "(", splits, "splits)")
        return splits
            
    def from_string(s):
        s = s.strip() # Convenience when reading from file or literals
        if s[0] != '[' or s[-1] != ']':
            raise ValueError(f'Illegal string in SnailfishNumber constructor: {s} (Needs to start with [ and end with ])')
        depth = 0
        for idx,c in enumerate(s[1:-3]):
            if c == '[':
                depth += 1
            elif c == ']':
                depth -= 1
            if depth < 0:
                raise ValueError(f'Illegal string in SnailfishNumber constructor: {s} (Negative depth encountered).')
            elif depth == 0:
                break
        # print("String:", s, "Left =", s[1:idx+2], "| Right =", s[idx+3:-1])
        s_left, s_right = s[1:idx+2], s[idx+3:-1]
        left  = SnailfishNumber.from_string(s_left)  if len(s_left) > 1 else int(s_left)
        right = SnailfishNumber.from_string(s_right) if len(s_right) > 1 else int(s_right)
        return SnailfishNumber(left, right)


t = SnailfishNumber() # Start with a zero
# with open('data/18_input_test2.txt', 'r') as file:
# with open('data/18_input_test1.txt', 'r') as file:
with open('data/18_input.txt', 'r') as file:
    for line in file:
        s = SnailfishNumber.from_string(line.strip())
        print(f"{t} + {s} =")
        # print("test:", str(s) == line.strip())
        t += s
        print(f"{t} (Magnitude {abs(t)})")
        print()

# for i in range(1,6):
    # t = SnailfishNumber(i, i)
    # s += t
    # print("t =", t)
    # print("s =", s)
    

# str_literals = """
# [1,1]
# [2,2]
# [3,3]
# [4,4]
# [5,5]
# [6,6]
# """

# s = SnailfishNumber() # Start with a zero
# for line in str_literals.split():
    # t = SnailfishNumber.from_string(line)
    # s += t
    # print("t =", t)
    # print("s =", s)

# a = SnailfishNumber.from_string('[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]')
# b = SnailfishNumber.from_string('[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]')
# c = a + b
# print(c) 
# d = SnailfishNumber.from_string('[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]')
# e = c + d
# print(e)
# f = SnailfishNumber.from_string('[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]')
# g = e + f
# print(g)



print(f"\nScript runtime = {datetime.datetime.now() - begin_time}s")

