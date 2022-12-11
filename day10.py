with open('./input10.txt') as f:
    data = f.read()
command_list = data.split('\n')[:-1]

total_signal_strength = 0
screen = ''
X_register = 1
cycle = 0
for line in command_list:
    iters = 1 + int(line[:3] == 'add')
    for _ in range(iters):
        screen += '#' if abs(X_register - cycle % 40) <= 1 else '.'
        cycle += 1
        if cycle % 40 == 20:
            total_signal_strength += X_register * cycle
        if cycle % 40 == 0:
            screen += '\n'
    n = int(line.split(' ')[1]) if line[:3] == 'add' else 0
    X_register += n

# part 1
print(total_signal_strength)

# part 2
print(screen)
