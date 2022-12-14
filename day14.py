with open('./input14.txt') as f:
    data = f.read()
rows = data.split('\n')[:-1]

def segment(pt1, pt2):
    [(x_min, x_max), (y_min, y_max)] = [tuple(sorted([pt1[i], pt2[i]])) for i in (0,1)]
    return [[i,j] for i in range(x_min, x_max+1) for j in range(y_min, y_max+1)]

rock_paths = [[[int(num) for num in pair.split(',')] for pair in line.split(' -> ')] for line in rows]
[max_x, max_y] = [max(point[i] for path in rock_paths for point in path) for i in (0,1)]

# part 1
field = [['.']*(max_x+1) for _ in range(max_y+1)]

for path in rock_paths:
    for k in range(len(path)-1):
        for [i,j] in segment(path[k], path[k+1]):
            field[j][i] = '#'

def drop_grain():
    i, j = 0, 500
    while any([field[i+1][k] == '.' for k in [j, j-1, j+1]]):
        i += 1
        j = [k for k in [j, j-1, j+1] if field[i][k] == '.'][0]
    field[i][j] = 'o'

grain_count = 0
finished = False
while not finished:
    try:
        drop_grain()
        grain_count += 1
    except:
        finished = True

print(grain_count)

# part 2
field = dict()
for path in rock_paths:
    for k in range(len(path)-1):
        for [x,y] in segment(path[k], path[k+1]):
            field[(y,x)] = '#'
for x in range(-500, 1500):
    field[(max_y+2, x)] = '#'

def drop_grain_dict():
    i, j = 0, 500
    while any([(i+1,k) not in field for k in [j, j-1, j+1]]):
        i += 1
        j = [k for k in [j, j-1, j+1] if (i, k) not in field][0]
    field[(i,j)] = 'o'

grain_count = 0
while (0, 500) not in field:
    drop_grain_dict()
    grain_count += 1

print(grain_count)
