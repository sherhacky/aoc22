with open('./input10.txt') as f:
    data = f.read()
rows = data.split('\n')[:-1]

# part 1

total_signal_strength = 0
x = 1
cycle = 0
for line in rows:
    repeat = 1 + int(line[0] == 'a')
    for _ in range(repeat):
        cycle += 1
        if cycle % 40 == 20:
            total_signal_strength += x*cycle
    n = int(line.split(' ')[1]) if line[0] == 'a' else 0
    x += n

print(total_signal_strength)

# part 2

screen = []
scanline = []
x = 1
cycle = 0
for line in rows:
    repeat = 1 + int(line[0] == 'a')
    for _ in range(repeat):
        scanline.append('#' if abs(x - cycle % 40) <= 1 else '.')
        cycle += 1
        if cycle % 40 == 0:
            screen.append(scanline)
            scanline = []
    n = int(line.split(' ')[1]) if line[0] == 'a' else 0
    x += n

for scanline in screen:
    print(''.join(scanline))