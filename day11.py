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

def get_monkey_business(iterations, worry_reducing_function):
    items, operation, test_divisible_by, target_monkey = initialize()
    monkey_count = [0]*len(items)
    for _ in range(iterations):
        for i in range(len(items)):
            monkey_count[i] += len(items[i])
            while items[i]:
                current_item = items[i].pop(0)
                current_item = eval(operation[i], {'old': current_item})
                current_item = worry_reducing_function(current_item)
                passes_test = (current_item % test_divisible_by[i] == 0)
                next_monkey = target_monkey[i][int(passes_test)]
                items[next_monkey].append(current_item)
    return prod(sorted(monkey_count)[-2:])

# part 1
print(get_monkey_business(20, lambda x: x // 3))

# part 2
test_divisible_by = initialize()[2]
modulus = prod(test_divisible_by)
print(get_monkey_business(10000, lambda x: x % modulus))
