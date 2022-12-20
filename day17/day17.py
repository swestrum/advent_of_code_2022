from typing import List
from collections import deque
from copy import deepcopy
from itertools import islice

def parse_rocks(rock_lines):
    current_rock = []
    rocks = deque(maxlen=5)
    for l in rock_lines:
        if not l.strip():
            current_rock
            rocks.append(deepcopy(current_rock))
            current_rock = []
        else:
            current_rock.append(l.strip())
    return rocks

def move_down(screen):
    new_screen = deepcopy(screen)
    new_screen.reverse()
    for i, s in enumerate(new_screen):
        if '@' in s:
            if i - 1 < 0:
                return True, screen
            for j, character in enumerate(s):
                if character == '@':
                    if new_screen[i - 1][j] == '#':
                        return True, screen
                    new_screen[i - 1] = new_screen[i - 1][:j] + '@' + new_screen[i - 1][j + 1:]
                    new_screen[i] = new_screen[i][:j] + '.' + new_screen[i][j + 1:]
    new_screen.reverse()
    return False, new_screen

def move_left(screen):
    new_screen = deepcopy(screen)
    for i, s in enumerate(new_screen):
        if '@' in s:
            left_at = s.find('@')
            if left_at - 1 < 0 or s[left_at - 1] == '#':
                return screen
            right_at = s.rfind('@')
            new_screen[i] = new_screen[i][:left_at - 1] + ('@' * (right_at - left_at + 1)) + '.' + new_screen[i][right_at + 1:]
    return new_screen

def move_right(screen):
    new_screen = deepcopy(screen)
    for i, s in enumerate(new_screen):
        if '@' in s:
            right_at = s.rfind('@')
            if right_at + 1 >= len(screen[0]) or s[right_at + 1] == '#':
                return screen
            left_at = s.find('@')
            new_screen[i] = new_screen[i][:left_at] + '.' + ('@' * (right_at - left_at + 1)) + new_screen[i][right_at + 2:]
    return new_screen

def place_rock(rock, screen, movement):
    for i in range(3):
        screen.appendleft('.......')
    screen = deque(rock) + screen
    resting = False
    movements_made = 0
    while not resting:
        next_movement = movement.popleft()
        if next_movement == '<':
            screen = move_left(screen)
        elif next_movement == '>':
            screen = move_right(screen)
        resting, screen = move_down(screen)
        movements_made += 1
        movement.append(next_movement)
    while screen[0] == '.......':
        screen.popleft()
    new_screen = []
    for s in screen:
        new_screen.append(s.replace('@', '#'))
    return deque(new_screen), movement, movements_made

def print_screen(screen):
    for s in screen:
        print(s)

movement_file = open("input.txt", "r")
movement_lines = movement_file.readlines()
movement = deque(movement_lines[0].strip(), maxlen=len(movement_lines[0].strip()))

rock_file = open("rocks.txt", "r")
rock_lines = rock_file.readlines()
rocks = parse_rocks(rock_lines)

screen = deque()

for rocks_fallen in range(2022):
    next_rock = rocks.popleft()
    screen, movement = place_rock(next_rock, screen, movement)
    rocks.append(next_rock)

print(f"PART ONE: {len(screen)}")

screen = deque()
rocks = parse_rocks(rock_lines)
num_rocks = len(rocks)
movement = deque(movement_lines[0].strip(), maxlen=len(movement_lines[0].strip()))
num_movements = len(movement)
movements_made = 0
repeating_guess = len(movement) * len(rocks)
total_rocks = float(1000000000000)
record = {}

for rocks_fallen in range(10000):
    if rocks_fallen % 1000 == 0:
        print(f"PROGRESS: {rocks_fallen}")
    next_rock = rocks.popleft()
    screen, movement, movements_made_now = place_rock(next_rock, screen, movement)
    movements_made += movements_made_now
    rocks.append(next_rock)
    current_height = len(screen)
    rock_index = rocks_fallen % num_rocks
    movement_index = movements_made % num_movements
    cycle_key = (rock_index, movement_index)
    if cycle_key in record.keys():
        r, h = record[cycle_key]
        rock_diff = rocks_fallen - r
        if rocks_fallen % rock_diff == total_rocks % rock_diff:
            print(f'Cycle of length {rock_diff} found (iterations {r} - {rocks_fallen})')
            cycle_height = current_height - h
            rocks_remaining = float(total_rocks - rocks_fallen)
            cycles_remaining = float(rocks_remaining // rock_diff) + 1
            extrapolated_height = h + (float(cycle_height) * float(cycles_remaining))
            break
    else:
        record[cycle_key] = (rocks_fallen, current_height)

    
print(f"PART TWO: {extrapolated_height - 1}")