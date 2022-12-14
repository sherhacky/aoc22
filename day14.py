from string import ascii_lowercase

with open('./input14.txt') as f:
    data = f.read()

datas = '''498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''
rows = data.split('\n')[:-1]


rock_paths = [[[int(num) for num in pair.split(',')] for pair in line.split(' -> ')] for line in rows]

maxes = (
    max(x for path in rock_paths for [x,y] in path),
    max(y for path in rock_paths for [x,y] in path),
)

lows = (
    min(x for path in rock_paths for [x,y] in path),
    min(y for path in rock_paths for [x,y] in path),
)

field = [['.']*(maxes[0]+1) for _ in range(maxes[1]+1)]


# print(field, lows)

def segment(pt1, pt2):
    x_min, x_max = tuple(sorted([pt1[0], pt2[0]]))
    y_min, y_max = min(pt1[1], pt2[1]), max(pt1[1], pt2[1])
    return [[i,j] for i in range(x_min, x_max+1) for j in range(y_min, y_max+1)]

for path in rock_paths:
    # print(path)
    for k in range(len(path)-1):
        # print(segment(path[k], path[k+1]))
        for [i,j] in segment(path[k], path[k+1]):
            # print(j,i)
            field[j][i] = '#'

# for y in range(10):
#     print(field[y][494:504])

rocks = {(x,y) for y in range(len(field)) for x in range(len(field[0])) if field[y][x] == '#'}
# print('rocks?')
# print(rocks)

def print_chunk(x,y):
    x_low = max(0, x-10)
    x_high = min(len(field[0]), x+10)
    y_low = max(0, y-1)
    y_high = min(len(field), y+2)
    for y in range(y_low, y_high):
        print(''.join(field[y][x_low:x_high]))

def drop_grain():
    i, j = 0, 500
    while any([field[i+1][k] == '.' for k in [j, j-1, j+1]]):
        i += 1
        j = [k for k in [j, j-1, j+1] if field[i][k] == '.'][0]
        # print(j,i)
        # print_chunk(j,i)
    field[i][j] = 'o'

grain_count = 0
finished = False
while not finished:
    try:
        drop_grain()
        grain_count += 1
    except:
        finished = True

# for y in range(10):
#     print(field[y][494:504])

print(grain_count)
# for y, level in enumerate(field):
#     if '#' in level:
#         print(y, level)

# print(field)

# print(segment([504,19], [508,19]))