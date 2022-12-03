
# A = X = Rock
# B = Y = Paper
# C = Z = Scissors

# Rock > Scissors
# Scissors > Paper
# Paper > Rock

def calc_round_score(elf_move, self_move):
    win_dict = {'X': 'C', 'Y': 'A', 'Z': 'B'}
    draw_dict = {'X': 'A', 'Y': 'B', 'Z': 'C'}

    select_score = {'X': 1, 'Y': 2, 'Z': 3}
    if elf_move == win_dict[self_move]:
        win_score = 6
    elif elf_move == draw_dict[self_move]:
        win_score = 3
    else:
        win_score = 0
    return select_score[self_move] + win_score

def calc_modified_score(elf_move, strategy):
    win_score = {'X': 0, 'Y': 3, 'Z': 6}

    win_dict = {'A':'B', 'B':'C', 'C':'A'}
    lose_dict = {'A':'C', 'B':'A', 'C':'B'}

    select_dict = {'A': 1, 'B': 2, 'C': 3}

    if strategy == 'X':
        selection = lose_dict[elf_move]
    elif strategy == 'Y':
        selection = elf_move
    else:
        selection = win_dict[elf_move]
    return select_dict[selection] + win_score[strategy]

strategy_file = open('input.txt', 'r')
strategy_lines = strategy_file.readlines()

total_score = 0

for s in strategy_lines:
    split_line = s.split(' ')
    total_score += calc_round_score(split_line[0], split_line[1].strip())

print(f"Part 1: {total_score}")

total_score = 0

for s in strategy_lines:
    split_line = s.split(' ')
    total_score += calc_modified_score(split_line[0], split_line[1].strip())

print(f"Part 2: {total_score}")