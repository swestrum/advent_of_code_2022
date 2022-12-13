from typing import List
import ast
from itertools import zip_longest
from functools import cmp_to_key

def parse_line(item):
    if not isinstance(item, int):
        parsed_items = ast.literal_eval(str(item))
        for i in parsed_items:
            i = parse_line(i)
        return parsed_items
    else:
        return item

def convert_compare_lines(left, right):
    ret_val = compare_lines(left, right)
    if ret_val:
        return -1
    else:
        return 1

def compare_lines(left, right):
    if left is None:
        return True
    elif right is None:
        return False
    elif isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        elif left > right: 
            return False
        elif left == right:
            return None
    elif isinstance(left, list) and isinstance(right, list):
        for l, r in zip_longest(left, right):
            ret_value = compare_lines(l, r)
            if ret_value is not None:
                return ret_value
    elif type(left) != type(right):
        if isinstance(left, int):
            return compare_lines([left], right)
        elif isinstance(right, int):
            return compare_lines(left, [right])

signal_file = open("input.txt", "r")
signal_lines = signal_file.readlines()

parsed_lines = [[]]
pairs = 0

for s in signal_lines:
    s = s.strip()
    if s:
        parsed_lines[pairs].append(parse_line(s))
    else:
        parsed_lines[-1] = tuple(parsed_lines[-1])
        parsed_lines.append([])
        pairs += 1

ordered_indices = 0

for i, pair in enumerate(parsed_lines):
    l,r = pair
    if compare_lines(l, r):
        ordered_indices += (i + 1)

print(f"PART ONE: {ordered_indices}")

ordered_packets = [[[2]],[[6]]]

for s in signal_lines:
    if s.strip():
        ordered_packets.append(parse_line(s.strip()))

new_ordered_packets = sorted(ordered_packets, key=cmp_to_key(convert_compare_lines))
decoder_key = (new_ordered_packets.index([[2]]) + 1) * (new_ordered_packets.index([[6]]) + 1)
print(f"PART TWO: {decoder_key}")