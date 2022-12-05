import string

with open('./input3.txt') as f:
    data = f.read()
rucksacks = data.split('\n')[:-1]

letters = string.ascii_lowercase + string.ascii_uppercase
rank = {char: i+1 for i,char in enumerate(letters)}

# part 1
total = 0
for inventory in rucksacks:
    mid = len(inventory)//2
    left, right = inventory[:mid], inventory[mid:]
    common_item = (set(left) & set(right)).pop()
    total += rank[common_item]
print(total)

# part 2
total = 0
for i in range(0, len(rucksacks), 3):
    common_badge = (set(rucksacks[i]) & set(rucksacks[i+1]) & set(rucksacks[i+2])).pop()
    total += rank[common_badge]
print(total)
