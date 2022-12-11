with open('./input11.txt') as f:
    data = f.read()

datad = '''Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''

monkey_chunks = data.split('\n\n')

print(monkey_chunks[-1])

items, operation, test_divisible_by, target_monkey = [], [], [], []

for i, chunk in enumerate(monkey_chunks):
    lines = chunk.split('\n')
    items.append([int(num) for num in lines[1].split(': ')[-1].split(', ')])
    operation.append(lines[2].split(' = ')[-1])
    test_divisible_by.append(int(lines[3].split(' ')[-1]))
    target_monkey.append((int(lines[5].split(' ')[-1]), int(lines[4].split(' ')[-1])))

monkey_count = [0]*len(items)
for _ in range(20):
    for i in range(len(items)):
        monkey_count[i] += len(items[i])
        while items[i]:
            current_item = items[i].pop(0)
            current_item = eval(operation[i], {'old': current_item})
            current_item //= 3
            items[target_monkey[i][int(current_item % test_divisible_by[i] == 0)]].append(current_item)
print(monkey_count)

monkey_business = sorted(monkey_count)[-1]*sorted(monkey_count)[-2]
print(monkey_business)
# for thing in (items, operation, test_divisible_by, target_monkey):
#     print(thing)

product = 1
for div in test_divisible_by:
    product*= div
print(product)

items, operation, test_divisible_by, target_monkey = [], [], [], []

for i, chunk in enumerate(monkey_chunks):
    lines = chunk.split('\n')
    items.append([int(num) for num in lines[1].split(': ')[-1].split(', ')])
    operation.append(lines[2].split(' = ')[-1])
    test_divisible_by.append(int(lines[3].split(' ')[-1]))
    target_monkey.append((int(lines[5].split(' ')[-1]), int(lines[4].split(' ')[-1])))

monkey_count = [0]*len(items)
for _ in range(10000):
    for i in range(len(items)):
        monkey_count[i] += len(items[i])
        while items[i]:
            current_item = items[i].pop(0)
            current_item = eval(operation[i], {'old': current_item})
            current_item %= product
            items[target_monkey[i][int(current_item % test_divisible_by[i] == 0)]].append(current_item)
    if _+1 in [1,20]+[1000*n for n in range(1, 11)]:
        print(_+1, monkey_count)


print(monkey_count)



monkey_business = sorted(monkey_count)[-1]*sorted(monkey_count)[-2]
print(monkey_business)

# monkey_count = [0]*len(items)
# residues = [[[item % divisor for divisor in test_divisible_by] for item in item_list] for item_list in items]
# for _ in range(10000):
#     for i in range(len(residues)):
#         monkey_count[i] += len(residues[i])
#         while residues[i]:
#             current_item = residues[i].pop(0)
#             current_item = [eval(operation[i], {'old': value}) for value in current_item]
#             print('before', current_item)
#             current_item = [current_item[k] % divisor for k, divisor in enumerate(test_divisible_by)]
#             print('after', current_item)
#             items[target_monkey[i][int(current_item[i] % test_divisible_by[i] == 0)]].append(current_item)

# print(monkey_count)

# monkey_business = sorted(monkey_count)[-1]*sorted(monkey_count)[-2]
# print(monkey_business)