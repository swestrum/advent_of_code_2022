from collections import defaultdict, deque
import numpy as np

def parse_cubes(cube_lines):
    cubes = []
    for c in cube_lines:
        cube = [int(c_idx) for c_idx in c.strip().split(',')]
        cubes.append(tuple(cube))
    return cubes

def create_sides(cube):
    sides = []
    sides.append((cube[0] - 0.5, cube[1]      , cube[2]      ))
    sides.append((cube[0] + 0.5, cube[1]      , cube[2]      ))
    sides.append((cube[0]      , cube[1] - 0.5, cube[2]      ))
    sides.append((cube[0]      , cube[1] + 0.5, cube[2]      ))
    sides.append((cube[0]      , cube[1]      , cube[2] - 0.5))
    sides.append((cube[0]      , cube[1]      , cube[2] + 0.5))
    return sides

def find_missing_cubes(cubes, max_dim):
    space = np.full((max_dim, max_dim, max_dim), -1)
    for x, y, z in cubes:
        space[x][y][z] = 1
    queue = deque([(0,0,0)])
    while queue:
        x, y, z = queue.popleft()
        if space[x + 1][y][z] == -1:
            space[x + 1][y][z] = 0
            queue.append((x + 1, y, z))
        if space[x - 1][y][z] == -1:
            space[x - 1][y][z] = 0
            queue.append((x - 1, y, z))
        if space[x][y + 1][z] == -1:
            space[x][y + 1][z] = 0
            queue.append((x, y + 1, z))
        if space[x][y - 1][z] == -1:
            space[x][y - 1][z] = 0
            queue.append((x, y - 1, z))
        if space[x][y][z + 1] == -1:
            space[x][y][z + 1] = 0
            queue.append((x, y, z + 1))
        if space[x][y][z - 1] == -1:
            space[x][y][z - 1] = 0
            queue.append((x, y, z - 1))
    m = np.where(space == -1)
    missing_cubes = []
    for i, _ in enumerate(m[0]):
        missing_cubes.append((m[0][i], m[1][i], m[2][i]))
    return missing_cubes
    
cube_file = open("input.txt", "r")
cube_lines = cube_file.readlines()

cubes = parse_cubes(cube_lines)

sides_parsed = defaultdict(lambda: 0)

for c in cubes:
    sides = create_sides(c)
    for s in sides:
        sides_parsed[s] += 1

exposed_sides = [s for s in sides_parsed.keys() if sides_parsed[s] <= 1]
num_exposed_sides = len(exposed_sides)

print(f"PART ONE: {num_exposed_sides}")

missing_cubes = find_missing_cubes(cubes, 22)
cubes += list(missing_cubes)

sides_parsed = defaultdict(lambda: 0)

for c in cubes:
    sides = create_sides(c)
    for s in sides:
        sides_parsed[s] += 1

exposed_sides = [s for s in sides_parsed.keys() if sides_parsed[s] <= 1]
num_exposed_sides = len(exposed_sides)

print(f"PART TWO: {num_exposed_sides}")