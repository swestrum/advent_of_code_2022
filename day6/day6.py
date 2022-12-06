def find_start_packet(message: str):
    i = 4
    start_set = start_str = message[0:i]
    while len(set(start_str)) != len(start_str):
        i += 1
        start_str = message[i - 4 : i]
    return i


def find_start_message(message: str):
    i = 14
    start_set = start_str = message[0:i]
    while len(set(start_str)) != len(start_str):
        i += 1
        start_str = message[i - 14 : i]
    return i


message_file = open("input.txt", "r")
message_lines = message_file.readlines()
message = message_lines[0]

print(f"Part 1: {find_start_packet(message)}")

print(f"Part 2: {find_start_message(message)}")
