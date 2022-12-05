with open('./input5.txt') as f:
    data = f.read()

[stacks, moves] = data.split('\n\n')
stacks = stacks.split('\n')[:-1]
moves = moves.split('\n')[:-1]
move_list = [[int(item) for item in row.split(' ')[1::2]] for row in moves] 

def fresh_stack():
    stack_list = [[] for i in range(9)]
    for row in stacks[::-1]:
        for i in range(9):
            entry = row[1 + 4*i]
            if entry != ' ':
                stack_list[i].append(entry)
    return stack_list

# part 1
stack_list = fresh_stack()
for [num, start, end] in move_list:
    for _ in range(num):
        stack_list[end-1].append(stack_list[start-1].pop())
print(''.join(stack[-1] for stack in stack_list))

# part 2
stack_list = fresh_stack()
for [num, start, end] in move_list:
    temp = []
    for _ in range(num):
        temp.append(stack_list[start-1].pop())
    stack_list[end-1] += temp[::-1]
print(''.join(stack[-1] for stack in stack_list))
