from typing import List


def build_dir_structure(directories_lines: List[str]):
    cwd = []
    dirs = {}
    parsing_dirs = False
    dir_size = 0
    for line in directories_lines:
        line = line.strip()
        if parsing_dirs:
            if "$" in line:
                dirs["/".join(cwd)[1:]] = dir_size
                for i in range(1, len(cwd)):
                    dirs["/".join(cwd[0:i])[1:]] += dir_size
                dir_size = 0
                parsing_dirs = False
            try:
                dir_size += int(line.split(" ")[0])
            except:
                pass
        if not parsing_dirs:
            if line == "$ cd ..":
                cwd.pop()
            elif "$ cd " in line:
                cwd.append(line.split(" ")[2])
                dirs["/".join(cwd)[1:]] = 0
            elif "$ ls" in line:
                parsing_dirs = True
    dirs["/".join(cwd)[1:]] = dir_size
    return dirs


directories_file = open("input.txt", "r")
directories_lines = directories_file.readlines()

dir_structure = build_dir_structure(directories_lines=directories_lines)

dir_sum = 0
for k, val in dir_structure.items():
    if val < 100000:
        dir_sum += val

print(f"PART 1: {dir_sum}")

smallest_dir = float("inf")
free_space = 70000000 - dir_structure[""]
required_space = 30000000 - free_space
for k, val in dir_structure.items():
    if val > required_space and val < smallest_dir:
        smallest_dir = val

print(f"PART 2: {smallest_dir}")
