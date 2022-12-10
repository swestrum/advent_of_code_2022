from typing import List
import numpy as np

def check_visible(trees, row, col):
    current_tree = trees[row][col]
    if current_tree > max(trees[row, :col]):
        return True
    if current_tree > max(trees[row, col + 1:]):
        return True
    if current_tree > max(trees[:row, col]):
        return True
    if current_tree > max(trees[row + 1:, col]):
        return True
    return False

def calc_scenic_score(trees, row, col):
    current_tree = trees[row][col]
    # Check right
    right_idx = np.where(trees[row, col + 1:] >= current_tree)[0]
    if right_idx.size > 0:
        right_score = min(right_idx) + 1
    else:
        right_score = len(trees[row]) - 1 - col
    # Check left
    left_idx = np.where(trees[row, :col] >= current_tree)[0]
    if left_idx.size > 0:
        left_score = col - max(left_idx)
    else:
        left_score = col
    # Check up
    up_idx = np.where(np.flip(trees[:row, col]) >= current_tree)[0]
    if up_idx.size > 0:
        up_score = min(up_idx) + 1
    else:
        up_score = row
    # Check down
    down_idx = np.where(trees[row + 1:, col] >= current_tree)[0]
    if down_idx.size > 0:
        down_score = min(down_idx) + 1
    else:
        down_score = len(trees) - 1 - row
    return right_score * left_score * up_score * down_score

def find_visible(tree_lines: List[List[int]]):
    visible_array = [
        [False for i in range(len(tree_lines[0]))] for j in range(len(tree_lines))
    ]
    visible_array[0] = [True for i in range(len(tree_lines[0]))]
    visible_array[len(visible_array) - 1] = [True for i in range(len(tree_lines[0]))]
    for i, _ in enumerate(visible_array):
        visible_array[i][0] = True
        visible_array[i][-1] = True
    
    visible_np = np.array(tree_lines)
    for col in range(1, len(tree_lines[0]) - 1):
        for row in range(1, len(tree_lines) - 1):
            if not visible_array[row][col]:
                if check_visible(visible_np, row, col):
                    visible_array[row][col] = True
    return visible_array

def calc_scenic_array(tree_lines):
    scenic_scores = np.zeros((len(tree_lines[0]), len(tree_lines)), dtype=int)

    scenic_np = np.array(tree_lines)
    for col in range(1, len(tree_lines[0]) - 1):
        for row in range(1, len(tree_lines) - 1):
            scenic_scores[row][col] = calc_scenic_score(scenic_np, row, col)
    
    return scenic_scores

trees_file = open("input.txt", "r")
tree_lines = trees_file.readlines()

tree_heights = []

for row in tree_lines:
    tree_heights.append([])
    for col in row.strip():
        tree_heights[-1].append(int(col))

visible_array = find_visible(tree_lines=tree_heights)
print(f"PART ONE: {sum([sum(v) for v in visible_array])}")

scenic_scores = calc_scenic_array(tree_lines=tree_heights)
print(f"PART TWO: {max([max(s) for s in scenic_scores])}")