"""
Your goal is to find the number of distinct paths that start at start, end at end, and don't visit small caves more than once. There are two types of caves: big caves (written in uppercase, like A) and small caves (written in lowercase, like b). It would be a waste of time to visit any small cave more than once, but big caves are large enough that it might be worth visiting them multiple times. So, all paths you find should visit small caves at most once, and can visit big caves any number of times.
"""

import numpy as np
import pandas as pd
import scipy
import datetime
from collections import defaultdict, deque, Counter

begin_time = datetime.datetime.now()

datafile = "Data/12_input.txt"
# datafile = "Data/12_input_test1.txt"
# datafile = "Data/12_input_test2.txt"
# datafile = "Data/12_input_test3.txt"


def read_cave_from_file(filename):
    # Kunne brukt defaultdict her for å gjøre det mer kompakt
    graph = dict()
    with open(filename, 'r') as file:
        for line in file:
            node1,node2 = line.strip().split('-')
            if node1 in graph.keys():
                graph[node1].append(node2)
            else:
                graph[node1] = [node2]
            if node2 in graph.keys():
                graph[node2].append(node1)
            else:
                graph[node2] = [node1]
    return graph

def is_big_cave(name):
    return name.isupper()
    
def is_small_cave(name):
    return name.islower() and name not in ('start', 'end')

def double_visit_available(path):
    counter = Counter(path)
    double_visits = [key for key in counter.keys() if is_small_cave(key) and counter[key] > 1]
    # print(path, counter, double_visits)
    return len(double_visits) < 1

def find_all_paths(graph):
    """Denne knota jeg mye med. Nøkkelen til å få det til å funke er å la hele veier ligge i køen
    i stedet for bare noder. Slik slipper man å spore seg tilbake langs grafen når man 
    """
    valid_paths = []
    queue = [['start']]
    while len(queue) > 0:
        current_path = queue.pop(0)
        current_node = current_path[-1]
        # print("Current path:", ','.join(current_path), ' | ', '-'.join(queue))
        # print("Current path", current_path, "Current node:", current_node)
        for child in graph[current_node]:
            # print("Considering child", child)
            if child == 'end':
                valid_paths += [current_path + [child]]
                # print("Found valid path:", current_path + [child])
            elif child.isupper() or (child not in ('start','end') and (child not in current_path or double_visit_available(current_path))):
                # print("Adding child", child, "to queue")
                queue.append(current_path + [child])
    return valid_paths
  

    
graph = read_cave_from_file(datafile)
print(graph)
paths = find_all_paths(graph)
# paths = breadth_first_search(graph)
# print('Final set of paths:')
# print('\n'.join([','.join(path) for path in sorted(paths)]))
print("Number of paths:", len(paths))



print(f"Script runtime = {datetime.datetime.now() - begin_time}s")

