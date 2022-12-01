calories_file = open('input2.txt', 'r')
calories_lines = calories_file.readlines()

calorie_total = []
for c in calories_lines:
    try:
        c = int(c)
        calorie_total[-1] += c
    except:
        calorie_total.append(0)

print(f"Calorie Total Max: {max(calorie_total)}")

top_three_total = 0
for i in range(3):
    max_calories = max(calorie_total)
    top_three_total += max_calories
    calorie_total.remove(max_calories)
    print(f"Got Max: {max_calories}")

print(f"Top Three Total: {top_three_total}")