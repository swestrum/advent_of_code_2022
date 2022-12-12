import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy

def create_paths(elevations):
    rows = len(elevations)
    cols = len(elevations[0])
    graph = nx.grid_graph(dim=[cols, rows])
    graph = graph.to_directed()
    for e in deepcopy(graph.edges):
        elevation_diff = elevations[e[0]] - elevations[e[1]]
        if elevation_diff < -1:
            graph.remove_edge(*e)
    return graph

def parse_elevation(elevation_lines):
    rows = len(elevation_lines)
    cols = len(elevation_lines[0].strip())
    elevations = np.empty([rows, cols])
    for i, line in enumerate(elevation_lines):
        for j, letter in enumerate(line.strip()):
            elevations[i][j] = ord(letter)
    return elevations

elevation_file = open("input.txt", "r")
elevation_lines = elevation_file.readlines()

elevations = parse_elevation(elevation_lines)

start = np.where(elevations == ord('S'))
start = (start[0][0], start[1][0])
end = np.where(elevations == ord('E'))
end = (end[0][0], end[1][0])

elevations[elevations == ord('S')] = ord('a')
elevations[elevations == ord('E')] = ord('z')

paths = create_paths(elevations)

print(f"PART ONE: {nx.shortest_path_length(paths, start, end)}")

potential_starts = np.where(elevations == ord('a'))

starts = []

for s in range(len(potential_starts[0])):
    starts.append((potential_starts[0][s], potential_starts[1][s]))

shortest_path = float('inf')

for s in starts:
    try:
        short = nx.shortest_path_length(paths, s, end)
    except:
        pass
    if short < shortest_path:
        shortest_path = short

print(f"PART TWO: {shortest_path}")