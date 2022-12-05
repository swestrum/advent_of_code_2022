from typing import List
import re
from copy import deepcopy

def populate_crates(crate_diagram: List[str], crate_labels: List[int]):
    crates = {l: [] for l in crate_labels}
    for crate_line in crate_diagram:
        for c in crates.keys():
            crate = crate_line[(c-1)*4:(c*4)].strip()
            if crate:
                crates[c].append(crate)
    return(crates)

def run_instructions(crate_list: List[List[str]], instructions: List[str]):
    for i in instructions:
        search = re.search('move (\d+) from (\d+) to (\d+)', i.strip())
        num_crates = int(search[1])
        start_loc = int(search[2])
        end_loc = int(search[3])
        for n in range(num_crates):
            moved_crate = crate_list[start_loc].pop()
            crate_list[end_loc].append(moved_crate)
    return crate_list

def run_instructions_new(crate_list: List[List[str]], instructions: List[str]):
    for i in instructions:
        search = re.search('move (\d+) from (\d+) to (\d+)', i.strip())
        num_crates = int(search[1])
        start_loc = int(search[2])
        end_loc = int(search[3])
        moved_crates = crate_list[start_loc][num_crates:]
        crate_list[start_loc] = crate_list[start_loc][:len(crate_list[start_loc]) - num_crates]
        crate_list[end_loc] += moved_crates
    return crate_list

crate_file = open('crates.txt', 'r')
crate_lines = crate_file.readlines()
crate_labels = crate_lines.pop().split('  ')
crate_labels = [int(c) for c in crate_labels]
crate_lines.reverse()
crate_lines = [c.strip() for c in crate_lines]

instruction_file = open('instructions.txt', 'r')
instruction_lines = instruction_file.readlines()

crates = populate_crates(crate_lines, crate_labels)

new_config = {k: c[-1] for k, c in run_instructions(deepcopy(crates), instruction_lines).items()}

print(f"Part 1: {new_config}")

new_config = run_instructions_new(deepcopy(crates), instruction_lines)
new_config = {k: c[-1] for k, c in new_config.items()}

print(f"Part 2: {new_config}")