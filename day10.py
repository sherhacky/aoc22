with open('./input10.txt') as f:
    data = f.read()

datas = '''addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
'''

rows = data.split('\n')[:-1]

total_signal_strength = 0

x = 1
cycle = 0
for line in rows:
    print(line)
    if line[0] == 'n':
        print(cycle, x)
        cycle += 1
        if cycle % 40 == 20:
            total_signal_strength += x*cycle
            print('check: ', cycle, x, x*cycle, total_signal_strength)

    else:
        n = int(line.split(' ')[1])
        for _ in range(2):
            print(cycle, x)
            cycle += 1
            if cycle % 40 == 20:
                total_signal_strength += x*cycle
                print('check: ', cycle, x, x*cycle, total_signal_strength)
        x += n
print(total_signal_strength)

screen = []
scanline = []
x = 1
cycle = 0
for line in rows:
    print(line)
    if line[0] == 'n':
        print(cycle, x)
        cycle += 1
        scanline.append('#' if abs(x - (cycle-1)%40) <= 1 else '.')
        if cycle % 40 == 0:
            screen.append(scanline)
            scanline = []
            

    else:
        n = int(line.split(' ')[1])
        for _ in range(2):
            print(cycle, x)
            cycle += 1
            scanline.append('#' if abs(x - (cycle-1)%40) <= 1 else '.')
            if cycle % 40 == 0:
                screen.append(scanline)
                scanline = []
        x += n
for scanline in screen:
    print(''.join(scanline))