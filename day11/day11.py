from typing import List
import operator
import math
from copy import deepcopy

def parse_monkey(monkey_str: List[str]):
    monkey_dict = {}
    monkey_dict['index'] = int(monkey_str[0].split(' ')[1].split(":")[0])
    monkey_items = monkey_str[1].split(': ')[1].split(", ")
    monkey_items = [int(x) for x in monkey_items]
    monkey_dict['operator'] = monkey_str[2].split('old ')[1].split(' ')
    try:
        monkey_dict['operator'][1] = int(monkey_dict['operator'][1])
    except:
        pass
    if monkey_dict['operator'][0] == '+':
        monkey_dict['operator'][0] = operator.add
    if monkey_dict['operator'][0] == '*':
        monkey_dict['operator'][0] = operator.mul
    monkey_dict['test_divisible'] = int(monkey_str[3].split('divisible by ')[1])
    monkey_dict['if_true'] = int(monkey_str[4].split('monkey ')[1])
    monkey_dict['if_false'] = int(monkey_str[5].split('monkey ')[1])
    return monkey_items, monkey_dict

def run_monkey_round(monkey_items, monkey):
    current_items = deepcopy(monkey_items[monkey['index']])
    activity = 0
    for item in current_items:
        worry_b = monkey['operator'][1]
        if worry_b == 'old':
            worry_b = item
        new_worry = monkey['operator'][0](item, worry_b)
        new_worry = math.floor(new_worry / 3)
        if new_worry % monkey['test_divisible'] == 0:
            monkey_items[monkey['if_true']].append(new_worry)
        else:
            monkey_items[monkey['if_false']].append(new_worry)
        monkey_items[monkey['index']].remove(item)
        activity += 1
    return activity, monkey_items

def run_complicated_monkey_round(monkey_items, monkey, divisors):
    current_items = deepcopy(monkey_items[monkey['index']])
    activity = 0
    for item in current_items:
        worry_b = monkey['operator'][1]
        new_worry = {}
        for k, v in item.items():
            if worry_b == 'old':
                new_worry[k] = (v * v) % k
            elif monkey['operator'][0] is operator.mul:
                new_worry[k] = (v * worry_b) % k
            else:
                new_worry[k] = (v + worry_b) % k
        if new_worry[monkey['test_divisible']] == 0:
            monkey_items[monkey['if_true']].append(new_worry)
        else:
            monkey_items[monkey['if_false']].append(new_worry)
        monkey_items[monkey['index']].remove(item)
        activity += 1
    return activity, monkey_items

def get_modulo(x, divisors):
    modulo = {}
    for d in divisors:
        modulo[d] = x % d
    return modulo

monkey_file = open("input.txt", "r")
monkey_lines = monkey_file.readlines()

monkey = []
monkies_parsed = []
monkey_items = []

for l in monkey_lines:
    l = l.strip()
    if l:
        monkey.append(l)
    else:
        monkey_item, monkey_parsed = parse_monkey(monkey)
        monkies_parsed.append(monkey_parsed)
        monkey_items.append(monkey_item)
        monkey = []

monkey_items_gold = deepcopy(monkey_items)

activity = [0] * 8

for i in range(20):
    for monkey_idx, monkey in enumerate(monkies_parsed):
        ind_act, monkey_items = run_monkey_round(monkey_items, monkey)
        activity[monkey_idx] += ind_act

max_activity = max(activity)
activity.remove(max_activity)
max_b_activity = max(activity)

print(f"PART ONE: {max_activity * max_b_activity}")

activity = [0] * 8
monkey_items = deepcopy(monkey_items_gold)

divisors = [m['test_divisible'] for m in monkies_parsed]

for m in range(len(monkey_items)):
    for i in range(len(monkey_items[m])):
        monkey_items[m][i] = get_modulo(monkey_items[m][i], divisors)

for i in range(10000):
    for monkey_idx, monkey in enumerate(monkies_parsed):
        ind_act, monkey_items = run_complicated_monkey_round(monkey_items, monkies_parsed[monkey_idx], divisors)
        activity[monkey_idx] += ind_act

print(activity)

max_activity = max(activity)
activity.remove(max_activity)
max_b_activity = max(activity)

print(f"PART TWO: {max_activity * max_b_activity}")