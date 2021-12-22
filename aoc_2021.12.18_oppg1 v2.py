"""
"""

import numpy as np
import pandas as pd
import scipy
import datetime
from collections import (defaultdict, deque)

begin_time = datetime.datetime.now()

class SnailfishNumber():
    """
    Version where each SnailfishNumber is recursively built up of left and right SnailfishNumbers
    """
    def __init__(self, l=[]):
        self.l = l
        self.reduce()
        
    def __str__(self):
        return self.l.__str__()

    def __add__(self, other):
        if len(self.l) == 0: # Definition of zero: self.l = []
            return other
        else:
            return SnailfishNumber([self.l, other.l])
        
    def find_bugs(self):
        return

    def max_depth(self):
        # return max(1 + self.left.max_depth(), 1 + self.right.max_depth())
        

    def reduce(self):
        # self.find_bugs()
        # while len(self.bugs) > 0:
            # bug = self.bugs.pop(0)
            # if bug['type'] == 'explode':
                # self.explode()
            # elif bug['type'] == 'split':
                # self.split()
        return
    
    def explode(self):
        return
        
    def split(self):
        return
            

s = SnailfishNumber()
print(s)
for i in range(1,6):
    t = SnailfishNumber([i,i])
    s += t
    print(s)
    

print(f"\nScript runtime = {datetime.datetime.now() - begin_time}s")

