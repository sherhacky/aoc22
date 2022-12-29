with open('./input24.txt') as f:
    data = f.read()


datas='''#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#
'''

datas='''#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
'''
rows = data.split('\n')[:-1]

m = len(rows)
n = len(rows[0])

def next_position(i, j, char):
    if char == '^':
        if rows[i-1][j] != '#':
            return i-1, j
        else:
            return m-2, j
    if char == '>':
        if rows[i][j+1] != '#':
            return i, j+1
        else:
            return i, 1
    if char == '<':
        if rows[i][j-1] != '#':
            return i, j-1
        else:
            return i, n-2
    if char == 'v':
        if rows[i+1][j] != '#':
            return i+1, j
        else:
            return 1, j

configuration = {(i,j): set([rows[i][j]]) for i in range(m) for j in range(n)}

print(configuration)

ground = set([(i,j) for (i,j) in configuration if rows[i][j] != '#'])
wall = set([(i,j) for (i,j) in configuration if rows[i][j] == '#'])
blizzard = {char: set([(i,j) for (i,j) in configuration if rows[i][j] == char]) for char in '<v^>'}

print(blizzard)
def print_board(reachable, blizzard):
    render_board = [[('#' if char == '#' else '.') for char in row] for row in rows]
    for (i, j) in reachable:
        render_board[i][j] = 'E'
    for (i,j) in ground:
        presence = [char for char in blizzard if (i,j) in blizzard[char]]
        if len(presence) == 1:
            render_board[i][j] = presence[0]
        if len(presence) > 1:
            render_board[i][j] = str(len(presence))
    for row in render_board:
        print(''.join(row))
    print('\n')


reachable = {(0,1)}
t = 0
print_board(reachable, blizzard)
while (m-1, n-2) not in reachable:
    for char in '<v^>':
        blizzard[char] = {next_position(i,j,char) for (i,j) in blizzard[char]}
    reachable = {(i+a, j+b) for (i, j) in reachable for (a,b) in [(1,0), (0,1), (-1,0), (0,-1), (0,0)] if all([
        (i+a, j+b) in ground
    ] + [
        (i+a, j+b) not in avoid_set for avoid_set in list(blizzard.values()) + [wall]
    ])}
    t += 1
    # print_board(reachable, blizzard)
print(t)

# part 2

reachable = {(m-1,n-2)}
while (0, 1) not in reachable:
    for char in '<v^>':
        blizzard[char] = {next_position(i,j,char) for (i,j) in blizzard[char]}
    reachable = {(i+a, j+b) for (i, j) in reachable for (a,b) in [(1,0), (0,1), (-1,0), (0,-1), (0,0)] if all([
        (i+a, j+b) in ground
    ] + [
        (i+a, j+b) not in avoid_set for avoid_set in list(blizzard.values()) + [wall]
    ])}
    t += 1
    # print_board(reachable, blizzard)
print(t)

reachable = {(0,1)}
while (m-1, n-2) not in reachable:
    for char in '<v^>':
        blizzard[char] = {next_position(i,j,char) for (i,j) in blizzard[char]}
    reachable = {(i+a, j+b) for (i, j) in reachable for (a,b) in [(1,0), (0,1), (-1,0), (0,-1), (0,0)] if all([
        (i+a, j+b) in ground
    ] + [
        (i+a, j+b) not in avoid_set for avoid_set in list(blizzard.values()) + [wall]
    ])}
    t += 1
    # print_board(reachable, blizzard)

print(t)