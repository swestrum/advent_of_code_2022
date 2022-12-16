import random
import time
from copy import deepcopy

from rich.live import Live
from rich.table import Table
from rich.console import Console


def generate_table(sand_placement, timestep) -> Table:
    """Make a new table."""
    table = Table()
    table.add_column(f"Sand Placement: {timestep}")

    for i, row in enumerate(sand_placement):
        table.add_row(f"{''.join(row)}")
    return table


def parse_wall(start, end):
    wall_placement = [start, end]
    if (start[0] - end[0]) != 0:
        for i in range(min(start[0], end[0]), max(start[0], end[0])):
            wall_placement.append((i, start[1]))
    else:
        for i in range(min(start[1], end[1]), max(start[1], end[1])):
            wall_placement.append((start[0], i))
    return set(wall_placement)


def parse_rock(sand_lines):
    rocks = []
    wall_height = 0
    wall_min = float('inf')
    wall_max = 0
    for s in sand_lines:
        s = s.strip()
        rocks.append(s.split(" -> "))
        parsed_rock = []
        for r in rocks[-1]:
            r = r.split(",")
            r = (int(r[0]), int(r[1]))
            if r[0] > wall_max:
                wall_max = r[0]
            if r[0] < wall_min:
                wall_min = r[0]
            if r[1] > wall_height:
                wall_height = r[1]
            parsed_rock.append(r)
        rocks[-1] = parsed_rock
    sand_row = ["."] * (wall_max - wall_min + 1)
    sand_placement = []
    for z in range(wall_height + 1):
        sand_placement.append(deepcopy(sand_row))
    sand_start = 500 - wall_min
    sand_placement[0][sand_start] = '+'
    for r in rocks:
        for i in range(1, len(r)):
            new_rocks = parse_wall(r[i - 1], r[i])
            for x, y in new_rocks:
                sand_placement[y][(x - 500) + sand_start] = '#'
    return sand_placement, sand_start


def add_sand(sand_placement, sand_start, floor=False):
    sand_place = (0, sand_start)
    resting = False
    while not resting:
        new_row = sand_place[0] + 1
        new_col = sand_place[1]
        if new_row == len(sand_placement):
            return sand_placement, -1
        if check_open(sand_placement, new_row, new_col):
            sand_place = (new_row, new_col)
        else:
            if new_col - 1 < 0:
                if floor:
                    for s in sand_placement:
                        s.insert(0, '.')
                    sand_placement[-1][0] = '#'
                    sand_start += 1
                else:
                    return sand_placement, -1
            if new_col + 1 >= len(sand_placement[0]):
                if floor:
                    for s in sand_placement:
                        s.append('.')
                    sand_placement[-1][-1] = '#'
                else:
                    return sand_placement, -1
            if check_open(sand_placement, new_row, new_col - 1):
                sand_place = (new_row, new_col - 1)
            elif check_open(sand_placement, new_row, new_col + 1):
                sand_place = (new_row, new_col + 1)
            else:
                sand_placement[sand_place[0]][sand_place[1]] = 'o'
                if sand_placement[0][sand_start] == 'o':
                    return sand_placement, -1
                resting = True
    return sand_placement, sand_start


def check_open(sand_placement, row, col):
    return sand_placement[row][col] == '.'


def add_floor(sand_placement):
    width = len(sand_placement[0])
    sand_placement.append(['.'] * width)
    sand_placement.append(['#'] * width)
    return sand_placement


sand_file = open("input.txt", "r")
sand_lines = sand_file.readlines()

sand_placement, sand_start = parse_rock(sand_lines=sand_lines)

for i in range(4000):
    sand_placement, sand_start = add_sand(sand_placement, sand_start)
    if sand_start < 0:
        print(f"PART ONE: {i}")
        break

sand_file = open("input.txt", "r")
sand_lines = sand_file.readlines()

sand_placement, sand_start = parse_rock(sand_lines=sand_lines)
sand_placement = add_floor(sand_placement)

for i in range(40000):
    sand_placement, sand_start = add_sand(sand_placement, sand_start, floor=True)
    if sand_start < 0:
        print(f"PART TWO: {i}")
        break