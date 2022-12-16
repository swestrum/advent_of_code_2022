import re
from typing import List, Dict, Any
from collections import defaultdict
from copy import deepcopy

def manhattan_distance(x1: int, y1: int, x2: int, y2: int):
    return abs(x1 - x2) + abs(y1 - y2)

def parse_line(line: str):
    re_matches = re.match(r'Sensor at x=([\d,-]+), y=([\d,-]+): closest beacon is at x=([\d,-]+), y=([\d,-]+)', line)
    return {'sensor': (int(re_matches[1]), int(re_matches[2])), 'beacon': (int(re_matches[3]), int(re_matches[4]))}

def no_beacons(parsed_sensors: List[Dict[str, Any]]):
    no_beacons = defaultdict(lambda:[])
    for s in parsed_sensors:
        dist = manhattan_distance(s['sensor'][0], s['sensor'][1], s['beacon'][0], s['beacon'][1])
        min_no_beacons = s['sensor'][0]
        max_no_beacons = s['sensor'][0] + 1
        for d in range(s['sensor'][1] - dist, s['sensor'][1]):
            no_beacons_row = (min_no_beacons, max_no_beacons)
            min_no_beacons -= 1
            max_no_beacons += 1
            no_beacons[d].append(no_beacons_row)
        for d in range(s['sensor'][1], s['sensor'][1] + dist + 1):
            no_beacons_row = (min_no_beacons, max_no_beacons)
            min_no_beacons += 1
            max_no_beacons -=1
            no_beacons[d].append(no_beacons_row)
    for s in parsed_sensors:
        no_beacons[s['sensor'][1]].append((None, s['sensor'][0]))
        no_beacons[s['beacon'][1]].append((None, s['beacon'][0]))
    return no_beacons

def merge_interval(interval_one, interval_two):
    if interval_one[1] < interval_two[0] or interval_one[0] > interval_two[1]:
        return [interval_one, interval_two]
    return [(min(interval_one[0], interval_two[0]), max(interval_one[1], interval_two[1]))]

def merge_ranges(no_beacon_ranges: List[Any]):
    last_len = float('inf')
    while last_len > len(no_beacon_ranges):
        last_len = len(no_beacon_ranges)
        no_beacon_ranges = sorted(no_beacon_ranges, key = lambda x: x[0])
        new_beacon_ranges = set()
        for i in range(1, len(no_beacon_ranges), 2):
            new_beacon_ranges = new_beacon_ranges.union(merge_interval(no_beacon_ranges[i-1], no_beacon_ranges[i]))
        if len(no_beacon_ranges) % 2 == 1:
            new_beacon_ranges = new_beacon_ranges.union([no_beacon_ranges[-1]])
        no_beacon_ranges = list(new_beacon_ranges)
    return no_beacon_ranges

def count_no_beacons(no_beacons: List[Any], row: int):
    no_beacon_ranges = [b for b in no_beacons[row] if b[0] is not None]
    beacons = [b[1] for b in no_beacons[row] if b[0] is None]
    no_beacon_ranges = merge_ranges(no_beacon_ranges)
    num_beacons = 0
    if len(no_beacon_ranges) > 1:
        for r in no_beacon_ranges:
            num_beacons += r[1] - r[0]
    else:
        num_beacons = no_beacon_ranges[0][1] - no_beacon_ranges[0][0]
    num_beacons -= len(set(beacons))
    return num_beacons

def find_distress_beacons(no_beacons: List[Any], max_x_y: int):
    potential_beacons = []
    for y, row in no_beacons.items():
        if y <= max_x_y and y > 0:
            no_beacon_ranges = [(max(b[0], 0), min(max_x_y, b[1])) for b in row if b[0] is not None]
            ranges = merge_ranges(no_beacon_ranges)
            if len(ranges) > 1:
                if ranges[0][0] > 0:
                    ranges.insert(0, (None, 0))
                if ranges[-1][-1] < max_x_y:
                    ranges.append((max_x_y, None))
                for i in range(1, len(ranges)):
                    for r in range(ranges[i-1][1], ranges[i][0]):
                        potential_beacons.append((r, y))
    return potential_beacons
            
    
sensor_file = open("input.txt", "r")
sensor_lines = sensor_file.readlines()

parsed_sensors = []

for l in sensor_lines:
    parsed_sensors.append(parse_line(l))

no_beacons = no_beacons(parsed_sensors)
interesting_row = 2000000
print("Counting beacons....")
print(f"PART ONE: {count_no_beacons(deepcopy(no_beacons), interesting_row)}")

print("Finding distress beacon....")
distress_beacon = find_distress_beacons(no_beacons, 4000000)
print(distress_beacon)
distress_beacon = distress_beacon[0]
tuning_frequency = distress_beacon[0] * 4000000 + distress_beacon[1]
print(f"PART TWO: {tuning_frequency}")