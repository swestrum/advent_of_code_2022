from typing import Iterable

def find_common_item(pack_list:str):
    pack_len = len(pack_list)
    compartment_1 = set(pack_list[0: pack_len//2])
    compartment_2 = set(pack_list[pack_len//2: pack_len])

    return compartment_1.intersection(compartment_2).pop()


def find_group_common_item(group_pack_list: Iterable[str]):
    group_pack_sets = []
    for p in group_pack_list:
        group_pack_sets.append(set(p))
    common_item = group_pack_sets.pop()
    for c in group_pack_sets:
        common_item = common_item.intersection(c)
    return common_item.pop()


def find_priority(item: str):
    if item.isupper():
        return ord(item) - 38
    else:
        return ord(item) - 96


packing_file = open('input.txt', 'r')
packing_lines = packing_file.readlines()

priority_sum = 0

for p in packing_lines:
    common_item = find_common_item(p)
    priority_sum += find_priority(common_item)

print(f"Part 1: {priority_sum}")

group_pack_list = []
priority_sum = 0

for p in packing_lines:
    if len(group_pack_list) == 3:
        common_item = find_group_common_item(group_pack_list)
        priority_sum += find_priority(common_item)
        group_pack_list = [p.strip()]
    else:
        group_pack_list.append(p.strip())

common_item = find_group_common_item(group_pack_list)
priority_sum += find_priority(common_item)

print(f"Part 2: {priority_sum}")