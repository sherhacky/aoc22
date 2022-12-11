from math import prod

with open('./input11.txt') as f:
    data = f.read()

monkey_chunks = data.split('\n\n')

def initialize():
    items, operation, test_divisible_by, target_monkey = [], [], [], []
    for i, chunk in enumerate(monkey_chunks):
        lines = chunk.split('\n')
        items.append([int(num) for num in lines[1].split(': ')[-1].split(', ')])
        operation.append(lines[2].split(' = ')[-1])
        test_divisible_by.append(int(lines[3].split(' ')[-1]))
        target_monkey.append((int(lines[5].split(' ')[-1]), int(lines[4].split(' ')[-1])))
    return items, operation, test_divisible_by, target_monkey

# part 1
items, operation, test_divisible_by, target_monkey = initialize()
monkey_count = [0]*len(items)
for _ in range(20):
    for i in range(len(items)):
        monkey_count[i] += len(items[i])
        while items[i]:
            current_item = items[i].pop(0)
            current_item = eval(operation[i], {'old': current_item})
            current_item //= 3
            items[target_monkey[i][int(current_item % test_divisible_by[i] == 0)]].append(current_item)

monkey_business = prod(sorted(monkey_count)[-2:])
print(monkey_business)

# part 2
items, operation, test_divisible_by, target_monkey = initialize()
monkey_count = [0]*len(items)

modulo = prod(test_divisible_by)

for _ in range(10000):
    for i in range(len(items)):
        monkey_count[i] += len(items[i])
        while items[i]:
            current_item = items[i].pop(0)
            current_item = eval(operation[i], {'old': current_item})
            current_item %= modulo
            items[target_monkey[i][int(current_item % test_divisible_by[i] == 0)]].append(current_item)

monkey_business = prod(sorted(monkey_count)[-2:])
print(monkey_business)
