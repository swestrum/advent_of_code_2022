from typing import List


def find_visible(tree_lines: List[str]):
    visible_array = [
        [False for i in range(len(tree_lines[0]))] for j in range(len(tree_lines))
    ]
    visible_array[0] = [True for i in range(len(tree_lines[0]))]
    visible_array[len(visible_array) - 1] = [True for i in range(len(tree_lines[0]))]
    for i, _ in enumerate(visible_array):
        visible_array[i][0] = True
        visible_array[i][-1] = True

    return visible_array


trees_file = open("input.txt", "r")
trees_lines = trees_file.readlines()

visible_array = find_visible(tree_lines=trees_lines)
print(sum([sum(v) for v in visible_array]))
