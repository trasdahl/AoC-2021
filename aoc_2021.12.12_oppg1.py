"""
Your goal is to find the number of distinct paths that start at start, end at end, and don't visit small caves more than once. There are two types of caves: big caves (written in uppercase, like A) and small caves (written in lowercase, like b). It would be a waste of time to visit any small cave more than once, but big caves are large enough that it might be worth visiting them multiple times. So, all paths you find should visit small caves at most once, and can visit big caves any number of times.
"""

import numpy as np
import pandas as pd
import scipy
import datetime
from collections import (defaultdict, deque)

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
        for node in graph[current_node]:
            if node == 'end':
                valid_paths += [current_path + [node]]
                # print("Found valid path:", current_path + [node])
            elif node.isupper() or node not in current_path:
                queue.append(current_path + [node])
    return valid_paths
  

# # Tidlig forsøk som ikke funket. Har noder i stedet for veier i køen.
# # Sliter med å spore seg riktig tilbake når den møter en endestasjon.
# def breadth_first_search(graph):
    # paths = []
    # queue = ['start']
    # path = []
    # while len(queue) > 0:
        # print(','.join(path), ' | ', '-'.join(queue))
        # current = queue.pop(0)
        # path.append(current)
        # if current == 'end':
            # print(f"Reached end. Path: {','.join(path)}")
            # paths.append(path.copy())
            # # Take enough steps back
            # while queue[0] not in graph[path[-1]]:
                # path.pop() # Take one step back
                # print("Step back to", path[-1])
            # # return path
        # else:
            # children_to_visit = [n for n in graph[current] if n.isupper() or n not in path]
            # if len(children_to_visit) > 0:
                # queue = children_to_visit + queue
                # # for n in children_to_visit[::-1]:
                    # # if neighbour.isupper() or neighbour not in path:
                        # # # queue.append(neighbour) # BFS
                        # # queue.insert(0, n)
            # else:
                # path.pop() # Take one step back
    # return paths

    
graph = read_cave_from_file(datafile)
print(graph)
paths = find_all_paths(graph)
# paths = breadth_first_search(graph)
# print('Final set of paths:')
# print('\n'.join([','.join(path) for path in sorted(paths)]))
print("Number of paths:", len(paths))

# sys.exit()


# # Algoritme funnet fra https://stackoverflow.com/questions/9535819/find-all-paths-between-two-graph-nodes
# # Funker bare på DAG, mens denne grafen er "betinget syklisk". På dette problemet går algoritmen
# # bare i loop uten å komme i mål.

# from collections import defaultdict

# # modified BFS
# def find_all_parents(G, s):
    # Q = [s]
    # parents = defaultdict(set)
    # n = 0
    # while len(Q) != 0:
        # v = Q[0]
        # Q.pop(0)
        # for w in G.get(v, []):
            # if v.isupper() or v not in parents[w]:
                # print(f"Adding parent {v} to {w}")
                # n += 1
                # if n == 20:
                    # return parents
                # parents[w].add(v)
            # Q.append(w)
    # return parents

# # recursive path-finding function (assumes that there exists a path in G from a to b)   
# def find_all_paths(parents, a, b):
    # return [a] if a == b else [y + '-' + b for x in list(parents[b]) for y in find_all_paths(parents, a, x)]

# all_paths = find_all_paths(find_all_parents(nodes, 'start'), 'start', 'end')
# print(all_paths)



print(f"Script runtime = {datetime.datetime.now() - begin_time}s")

