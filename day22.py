with open('./input22.txt') as f:
    data = f.read()


datas = '''    .......#
    ....#...
    ...#....
    ......#.
    ...#
    ....
    ..#.
    ....
...#....
.....#..
.#......
......#.
...#
.#..
#...
....

10R5L5R10L4R5L5
'''
board = data.split('\n\n')[0].split('\n')
instructions = data.split('\n')[-2]
m = len(board[0])
for i, line in enumerate(board):
    board[i] += ' '*(m - len(board[i]))

# for line in board:
#     print(line, 'EOL')


cursor = {(0,1):'^', (-1,0):'<', (1,0):'>', (0,-1):'v'}
board_rendered = [[char for char in line] for line in board]

def record_position_at(position, orientation):
    x,y = position
    board_rendered[len(board) - 1 - y][x] = cursor[orientation]

def board_value_at(x,y):
    x,y = x%len(board[0]), y%len(board)
    # print('checking board value:')
    # print('x,y=', x, y)
    # print('looking at i,j =', len(board)-1-y, x)
    # print(len(board))
    # print(len(board[0]))
    return board[len(board) - 1 - y][x]




def move(position, orientation):
    x,y = position
    u,v = orientation
    next_position = ((x+u) % len(board[0]), (y+v) % len(board))
    if board_value_at(x+u, y+v) == ' ':
        # print('looking beyond')
        s,t = u, v
        while board_value_at(x+s, y+t) == ' ':
            s,t = s+u,t+v
        next_position = x+s, y+t
        # print('next: ', next_position, board_value_at(*next_position))
    next_position = (next_position[0] % len(board[0]), next_position[1] % len(board))
    if board_value_at(*next_position) == '.':
        return next_position
    else:
        return position

def turn(orientation, direction):
    x,y = orientation
    if direction == 'R':
        return (y, -x)
    if direction == 'L':
        return (-y, x)


def move_following(starting_position, starting_orientation, instructions):
    current_position = starting_position
    current_orientation = starting_orientation
    i = 0
    while i in range(len(instructions)):
        record_position_at(current_position, current_orientation)
        # ', current_position, current_orientation)
        if instructions[i] in 'LR':
           #  print('turn:', instructions[i])
            current_orientation = turn(current_orientation, instructions[i])
            i += 1
        else: 
            j = min([k for k in range(i+1, len(instructions)) if instructions[k] in 'LR'], default = len(instructions))
            number_of_steps = int(instructions[i:j])
            # print('go', number_of_steps)
            for _ in range(number_of_steps):
                record_position_at(current_position, current_orientation)
                current_position = move(current_position, current_orientation)
            i = j
        # current_position = (current_position[0] % len(board[0]), current_position[1] % len(board))
        # print('\n'.join([''.join(line) for line in board_rendered]))
    return current_position, current_orientation

starting_position = (min([j for j, item in enumerate(board[0]) if board[0][j] == '.']), len(board) - 1)
starting_orientation = (1, 0)

result = move_following(starting_position, starting_orientation, instructions)

final_position, final_orientation = result

print(result)
direction_value = {(1,0):0, (0,-1):1, (-1,0): 2, (0,1):3}
final_row = len(board) - final_position[1]
print('final row: ', final_row)
final_column = final_position[0] + 1
print('final column: ', final_column)
final_password = 1000*final_row + 4*final_column + direction_value[final_orientation]
print('final password: ', final_password)

def sgn(a):
    return a // abs(a) if a else 0

def linear_interpolation(point_1, point_2):
    x_1, y_1 = point_1
    x_2, y_2 = point_2
    u, v = sgn(x_2 - x_1), sgn(y_2 - y_1)
    return [(x_1 + i*u, y_1 + i*v) for i in range(max(abs(x_2-x_1), abs(y_2-y_1)) + 1)]

edge_cases = dict()

def flip(orientation):
    return tuple([-1*d for d in orientation])

def join_edges(start_1, end_1, start_2, end_2, ornt_before, ornt_after):
    seg1 = linear_interpolation(start_1, end_1)
    seg2 = linear_interpolation(start_2, end_2)
    # print('seg1', seg1)
    # print('seg2', seg2)
    for i in range(len(seg1)):
        edge_cases[(seg1[i], ornt_before)] = (seg2[i], ornt_after)
        edge_cases[(seg2[i], flip(ornt_after))] = (seg1[i], flip(ornt_before))


s = max(len(board), len(board[0])) // 4

print('cube side is {}'.format(s))

segment_joins = [
     ((s, 4*s-1), (2*s-1, 4*s-1),
      (0, s-1), (0, 0),
      (0, 1), (1, 0)),
     ((2*s, 4*s - 1), (3*s-1, 4*s - 1),
      (0, 0), (s-1, 0),
      (0, 1), (0, 1)),
     ((s, 3*s), (s, 4*s-1),
      (0, 2*s-1), (0, s),
      (-1, 0), (1, 0)),
     ((3*s-1, 3*s), (3*s-1, 4*s-1),
      (2*s-1, 2*s-1), (2*s-1, s),
      (1, 0), (-1, 0)),
     ((2*s, 3*s), (3*s-1, 3*s),
      (2*s-1, 3*s-1), (2*s-1, 2*s),
      (0, -1), (-1, 0)),
     ((s, 2*s), (s, 3*s-1),
      (s-1, 2*s-1), (0, 2*s-1),
      (-1, 0), (0, -1)),
     ((s, s), (2*s-1, s),
      (s-1, s-1), (s-1, 0),
      (0, -1), (-1, 0)),
    ]

for pairing in segment_joins:
    join_edges(*pairing)

def move_along_cube(position, orientation):
    x,y = position
    u,v = orientation
    if (position, orientation) in edge_cases:
        print('edge case found: ', position)
        next_position, next_orientation = edge_cases[(position, orientation)]
        print('next', next_position)
    else:
        next_position = (x+u, y+v)
        next_orientation = orientation
    if board_value_at(*next_position) == '.':
        return next_position, next_orientation
    else:
        return position, orientation

def traverse_cube(starting_position, starting_orientation, instructions):
    current_position = starting_position
    current_orientation = starting_orientation
    i = 0
    while i < len(instructions):
        record_position_at(current_position, current_orientation)
        if instructions[i] in 'LR':
            #print('turn:', instructions[i])
            current_orientation = turn(current_orientation, instructions[i])
            i += 1
        else: 
            j = min([k for k in range(i+1, len(instructions)) if instructions[k] in 'LR'], default = len(instructions))
            number_of_steps = int(instructions[i:j])
            #print('go', number_of_steps)
            for _ in range(number_of_steps):
                record_position_at(current_position, current_orientation)
                current_position, current_orientation = move_along_cube(current_position, current_orientation)
            i = j
        # current_position = (current_position[0] % len(board[0]), current_position[1] % len(board))
        #print('\n'.join([''.join(line) for line in board_rendered]))
    return current_position, current_orientation

board_rendered = [[char for char in line] for line in board]


starting_position = (min([j for j, item in enumerate(board[0]) if board[0][j] == '.']), len(board) - 1)
starting_orientation = (1, 0)

final_position, final_orientation = traverse_cube(starting_position, starting_orientation, instructions)

print(result)
direction_value = {(1,0):0, (0,-1):1, (-1,0): 2, (0,1):3}
final_row = len(board) - final_position[1]
print('final row: ', final_row)
final_column = final_position[0] + 1
print('final column: ', final_column)
final_password = 1000*final_row + 4*final_column + direction_value[final_orientation]
print('final password: ', final_password)
