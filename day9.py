with open('./input9.txt') as f:
    data = f.read()
rows = data.split('\n')[:-1]

dirs = {'R': (1, 0), 'U': (0, 1), 'L': (-1, 0), 'D': (0, -1)}

def shift(P, direction):
    return P[0] + dirs[direction][0], P[1] + dirs[direction][1]

def sgn(i):
    return i//max(abs(i),1)

def update(H, T):
    if max(abs(H[0] - T[0]), abs(H[1] - T[1])) > 1:
        return T[0] + sgn(H[0] - T[0]), T[1] + sgn(H[1] - T[1])
    return T

# part 1
H, T = (0, 0), (0, 0)
visited_positions = set()

for row in rows:
    [direction, count] = row.split(' ')
    for _ in range(int(count)):
        H = shift(H, direction)
        T = update(H, T)
        visited_positions.add(T)

print(len(visited_positions))

# part 2
knots = [(0,0) for i in range(10)]
visited_positions = set()

for row in rows:
    [direction, count] = row.split(' ')
    for _ in range(int(count)):
        knots[0] = shift(knots[0], direction)
        for i in range(len(knots)-1):
            knots[i+1] = update(knots[i], knots[i+1])
        visited_positions.add(knots[-1])

print(len(visited_positions))
