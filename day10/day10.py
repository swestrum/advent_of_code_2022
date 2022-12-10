from typing import List

def perform_instructions(instruction_lines: List[str]):
    x_register = []
    last_x = 1
    for l in instruction_lines:
        l = l.strip()
        if l == 'noop':
            x_register.append(last_x)
        else:
            instruction, v = l.split(' ')
            v = int(v)
            x_register.append(last_x)
            x_register.append(last_x)
            last_x += v
    return x_register

def calculate_crt(x_register: List[int]):
    crt = []
    for i, x in enumerate(x_register):
        horiz_position = i % 40
        if horiz_position == 0:
            crt.append("")
        if x in range(horiz_position - 1, horiz_position + 2):
            crt[-1] += "#"
        else:
            crt[-1] += "."
    return crt

instruction_file = open("input.txt", "r")
instruction_lines = instruction_file.readlines()

x_register = perform_instructions(instruction_lines)
# during the 20th, 60th, 100th, 140th, 180th, and 220th cycles
check_cycles = [20, 60, 100, 140, 180, 220]
part_one = 0
for c in check_cycles:
    part_one += x_register[c - 1] * c
print(f"PART ONE: {part_one}")

crt = calculate_crt(x_register)
print("PART TWO: ")
for c in crt:
    print(c)