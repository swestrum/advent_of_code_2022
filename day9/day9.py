from typing import List
from copy import deepcopy

def calc_tail_move(head_diff, head_position, tail_position):
    if tail_position[0] in range(head_position[0] - 1, head_position[0] + 2) and tail_position[1] in range(head_position[1] - 1, head_position[1] + 2):
        return tail_position
    if tail_position[0] != head_position[0] and tail_position[1] != head_position[1]:
        tail_position = [tail_position[0] + head_diff[0], tail_position[1] + head_diff[1]]
        if head_diff[0] and not head_diff[1]:
            tail_position[1] = head_position[1]
        if head_diff[1] and not head_diff[0]:
            tail_position[0] = head_position[0]
        return tail_position
    if tail_position[0] < head_position[0] - 1:
        tail_position[0] += 1
    elif tail_position[0] > head_position[0] + 1:
        tail_position[0] -= 1
    if tail_position[1] < head_position[1] - 1:
        tail_position[1] += 1
    elif tail_position[1] > head_position[1] + 1:
        tail_position[1] -= 1
    return tail_position

def calc_tail_positions(rope_lines):
    tail_positions = [(0,0)]
    tail_position = [0,0]
    head_position = [0,0]
    for l in rope_lines:
        direction, num = l.strip().split(' ')
        for i in range(int(num)):
            if direction == 'L':
                head_position[1] -= 1
                head_diff = [0, -1]
            elif direction == 'R':
                head_position[1] += 1
                head_diff = [0, 1]
            elif direction == 'U':
                head_position[0] -= 1
                head_diff = [-1, 0]
            elif direction == 'D':
                head_position[0] += 1
                head_diff = [1, 0]
            tail_position = calc_tail_move(head_diff, head_position, tail_position)
            tail_positions.append(tuple(tail_position))
    return len(set(tail_positions))

def calc_long_tail_positions(rope_lines):
    tail_positions = [(0,0)]
    rope_positions = [[0,0] for i in range(10)]
    for l in rope_lines:
        direction, num = l.strip().split(' ')
        for i in range(int(num)):
            if direction == 'L':
                rope_positions[0][1] -= 1
                head_diff = [0, -1]
            if direction == 'R':
                rope_positions[0][1] += 1
                head_diff = [0, 1]
            if direction == 'U':
                rope_positions[0][0] -= 1
                head_diff = [-1, 0]
            if direction == 'D':
                rope_positions[0][0] += 1
                head_diff = [1, 0]
            for i, knot in enumerate(rope_positions[1:]):
                new_position = calc_tail_move(head_diff, rope_positions[i], deepcopy(knot))
                head_diff = [new_position[0] - knot[0], new_position[1] - knot[1]]
                rope_positions[i + 1] = deepcopy(new_position)
            tail_positions.append(tuple(rope_positions[-1]))
    return len(set(tail_positions))

rope_file = open("input.txt", "r")
rope_lines = rope_file.readlines()

print(f"PART ONE: {calc_tail_positions(rope_lines)}")
print(f"PART TWO: {calc_long_tail_positions(rope_lines)}")