from typing import Iterable

def is_subset(list_one: Iterable[int], list_two: Iterable[int]):
    set_one = set(list_one)
    set_two = set(list_two)
    return set_one.issubset(set_two) or set_two.issubset(set_one)

def is_overlap(list_one: Iterable[int], list_two: Iterable[int]):
    set_one = set(list_one)
    set_two = set(list_two)
    return set_one.intersection(set_two) or set_two.intersection(set_one)

def determine_ranges(spec: str):
    range_strings = spec.split(",")
    ranges = []
    for r in range_strings:
        r_min, r_max = r.split("-")
        ranges.append(list(range(int(r_min), int(r_max) + 1)))
    return ranges

assignment_file = open('input.txt', 'r')
assignment_lines = assignment_file.readlines()

subsets = 0

for a in assignment_lines:
    ranges = determine_ranges(a.strip())
    if is_subset(*ranges):
        subsets += 1

print(f"Part 1: {subsets}")

intersects = 0

for a in assignment_lines:
    ranges = determine_ranges(a.strip())
    if is_overlap(*ranges):
        intersects += 1

print(f"Part 2: {intersects}")