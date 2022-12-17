import re
import networkx as nx
from itertools import permutations
from typing import Dict, Set, Any

def parse_line(line: str):
    re_matches = re.match(r'Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z,\,\ ]+)', line)
    return {re_matches[1]: {'rate': int(re_matches[2]), 'end_nodes': re_matches[3].split(", ")}}

def build_tunnel_network(tunnels):
    G = nx.Graph()
    for i, t in tunnels.items():
        G.add_node(i)
    for i, t in tunnels.items():
        for e in t['end_nodes']:
            G.add_edge(i, e)
    return G

def build_paths(start_node: str, opened_valves: Dict[str, int], unvisited: Set[str], shortest_paths: Dict[Any, int], timestep: int=0, time_limit: int=30):
    if timestep >= time_limit or not unvisited:
        yield {**opened_valves, **{start_node: timestep}}
    else:
        for v in unvisited:
            yield from build_paths(v, {**opened_valves, **{start_node: timestep}}, unvisited - {v}, shortest_paths, timestep + shortest_paths[(start_node, v)], time_limit)

def get_path_scores(feasible_paths, time_limit, unvisited_nodes, rates):
    scores = []
    for path in feasible_paths:
        path_value = 0
        for valve, time in path.items():
            if time <= time_limit:
                path_value += ((time_limit - time) * rates[valve])
        scores.append(([x for x in unvisited_nodes if x not in path], path_value))
    scores = sorted(scores, key=lambda x:x[1], reverse=True)
    return scores

tunnels_file = open("input.txt", "r")
tunnels_lines = tunnels_file.readlines()

tunnels = {}

for l in tunnels_lines:
    tunnels.update(parse_line(l.strip()))

tunnel_graph = build_tunnel_network(tunnels)
unvisited_nodes = set([chamber for chamber, info in tunnels.items() if info['rate'] > 0])
shortest_paths = {}
for i in unvisited_nodes | {'AA'}:
    for j in unvisited_nodes | {'AA'}:
        shortest_paths[(i,j)] = len(nx.shortest_path(tunnel_graph, i, j))
rates = {chamber: info['rate'] for chamber, info in tunnels.items()}

feasible_paths_part_one = build_paths(start_node="AA", opened_valves={}, unvisited=unvisited_nodes, shortest_paths=shortest_paths)
scores = get_path_scores(feasible_paths_part_one, 30, unvisited_nodes, rates)
_, max_pressure = scores[0]

print(f"PART ONE: {max_pressure}")

feasible_paths_part_two = build_paths(start_node="AA", opened_valves={}, unvisited=unvisited_nodes, shortest_paths=shortest_paths, timestep=0, time_limit=26)
scores = get_path_scores(feasible_paths_part_two, 26, unvisited_nodes, rates)
double_scores = []

for sub_unvisited, score in scores[:500]:
    potential_subpaths = build_paths(start_node="AA", opened_valves={}, unvisited=set(sub_unvisited), shortest_paths=shortest_paths, timestep=0, time_limit=26)
    sub_scores = []
    for subpath in potential_subpaths:
        subpath_value = 0
        for valve, time in subpath.items():
            if time <= 26:
                subpath_value += ((26 - time) * rates[valve])
        sub_scores.append(subpath_value)
    double_scores.append(score + max(sub_scores))

print(f"PART TWO: {max(double_scores)}")