with open('./input22.txt') as f:
    data = f.read()

sample_data='''        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
'''

board = data.split('\n\n')[0].split('\n')
instructions = data.split('\n')[-2]

n = max([len(row) for row in board])
for i, line in enumerate(board):
    board[i] += ' '*(n - len(board[i]))


def record_position_at(board_rendered, position, orientation):
    cursor = {(-1,0):'^', (0,-1):'<', (0,1):'>', (1,0):'v'}
    i,j = position
    board_rendered[i][j] = cursor[orientation]


# part 1

def move(board, position, orientation):
    m,n = len(board),len(board[0])
    i,j = position
    u,v = orientation
    next_position = ((i+u) % m, (j+v) % n)
    if board[next_position[0]][next_position[1]] == ' ':
        s,t = u, v
        while board[(i+s) % m][(j+t) % n] == ' ':
            s,t = s+u,t+v
        next_position = (i+s) % m, (j+t) % n
    next_position = (next_position[0] % len(board), next_position[1] % len(board[0]))
    if board[next_position[0]][next_position[1]] == '.':
        return next_position
    else:
        return position

def turn(orientation, direction):
    i,j = orientation
    x,y = j,-i
    if direction == 'R':
        result_p = (y, -x)
    if direction == 'L':
        result_p = (-y, x)
    x,y = result_p
    return -y,x


def traverse_route(starting_position, starting_orientation, instructions):
    board_rendered = [[char for char in line] for line in board]
    current_position = starting_position
    current_orientation = starting_orientation
    i = 0
    while i in range(len(instructions)):
        record_position_at(board_rendered, current_position, current_orientation)
        if instructions[i] in 'LR':
            current_orientation = turn(current_orientation, instructions[i])
            i += 1
        else: 
            j = min([k for k in range(i+1, len(instructions)) if instructions[k] in 'LR'], default = len(instructions))
            number_of_steps = int(instructions[i:j])
            for _ in range(number_of_steps):
                record_position_at(board_rendered, current_position, current_orientation)
                current_position = move(board, current_position, current_orientation)
            i = j
    print('\n'.join([''.join(line) for line in board_rendered]))
    return current_position, current_orientation

starting_position = (0, min([j for j, item in enumerate(board[0]) if board[0][j] == '.']))
starting_orientation = (0, 1)

result = traverse_route(starting_position, starting_orientation, instructions)

final_position, final_orientation = result

direction_value = {(0,1):0, (1,0):1, (0,-1): 2, (-1,0):3}
final_row = final_position[0] + 1
print('final row: ', final_row)
final_column = final_position[1] + 1
print('final column: ', final_column)
final_password = 1000*final_row + 4*final_column + direction_value[final_orientation]
print('final password: ', final_password)


# part 2

def sgn(a):
    return a // abs(a) if a else 0


def linear_interpolation(point_1, point_2):
    x_1, y_1 = point_1
    x_2, y_2 = point_2
    u, v = sgn(x_2 - x_1), sgn(y_2 - y_1)
    return [(x_1 + i*u, y_1 + i*v) for i in range(max(abs(x_2-x_1), abs(y_2-y_1)) + 1)]


def flip(orientation):
    return tuple([-1*d for d in orientation])


def join_edges(start_1, end_1, start_2, end_2, edge_dict):
    s = max([abs(end_1[i] - start_1[i])+1 for i in [0,1]])
    ornt_1 = edge_orientation(s, start_1, end_1)
    ornt_2 = edge_orientation(s, start_2, end_2)
    seg1 = linear_interpolation(start_1, end_1)
    seg2 = linear_interpolation(start_2, end_2)
    for i in range(len(seg1)):
        edge_dict[(seg1[i], ornt_1)] = (seg2[i], flip(ornt_2))
        edge_dict[(seg2[i], ornt_2)] = (seg1[i], flip(ornt_1))


def side_length(board):
    m, n = len(board), len(board[0])
    [l, w] = [max(m, n), min(m, n)]
    if 2*l == 5*w:
        s = l//5
    elif 3*l == 4*w:
        s = l//4
    return s


def edge_orientation(s, face_corner_1, face_corner_2):
    i, j = face_corner_1
    k, l = face_corner_2
    if j == l:
        if j % s == 0:
            return (0, -1)
        else:
            return (0, 1)
    elif i == k:
        if i % s == 0:
            return (-1, 0)
        else:
            return (1, 0)


def adjacent_face_corners(board, i, j):
    s = side_length(board)
    nbrs = empty_corner_nbrs(board, s, i, j)
    result = []
    for a, b in nbrs:
        if a == i:
            shift = s-1 if i % s == 0 else 1-s
            result.append((i + shift, j))
        if b == j:
            shift = s-1 if j % s == 0 else 1-s
            result.append((i, j + shift))
    return result


def empty_corner_nbrs(board, s, i, j):
    a = -1 if i % s == 0 else 1
    b = -1 if j % s == 0 else 1
    return [(u,v) for (u,v) in [(i+a, j), (i, j+b)] if not(0 <= u < len(board)) or not(0 <= v < len(board[0])) or board[u][v] == ' ']


def get_partition_element_containing(point, partition):
    for piece in partition:
        if point in piece:
            return piece
    return None


def get_corners_of_folded_cube(board):
    m, n = len(board), len(board[0])
    s = side_length(board)
    corners = set()
    for i in range(0, m+1, s):
        for j in range(0, n+1, s):
            this_corner = []
            for a in [0, -1]:
                for b in [0, -1]:
                    if 0 <= i + a < m and 0 <= j + b < n and board[i + a][j + b] != ' ':
                        this_corner.append((i + a, j + b))
            if any(this_corner):
                corners.add(frozenset(this_corner))
    while any([len(corner) != 3 for corner in corners]):
        complete_corners = [pointset for pointset in corners if len(pointset) == 3]
        for corner in complete_corners:
            next_corners = set()
            for i, j in corner:
                for a, b in adjacent_face_corners(board, i, j):
                    candidate = get_partition_element_containing((a,b), corners)
                    if len(candidate) != 3:
                        next_corners.add(candidate)
            if any(next_corners):
                new_corner = frozenset([pt for ptset in next_corners for pt in ptset])
                if new_corner not in corners:
                    for partial_corner in next_corners:
                        corners.discard(partial_corner)
                    corners.add(new_corner)
                    break
    return corners


def paste_cube_edges(board):
    edge_cases = dict()
    cube_corners = get_corners_of_folded_cube(board)
    s = side_length(board)
    for corner in cube_corners:
        for (i1,j1) in corner:
            for (i2,j2) in corner:
                if (i1,j1) != (i2,j2):
                    for (k1,l1) in adjacent_face_corners(board, i1, j1):
                        for (k2,l2) in adjacent_face_corners(board, i2, j2):
                            if get_partition_element_containing((k1, l1), cube_corners) == get_partition_element_containing((k2, l2), cube_corners):
                                join_edges((i1,j1), (k1,l1), (i2,j2), (k2,l2), edge_cases)
    return edge_cases


def move_along_cube(board, position, orientation, edge_cases):
    i,j = position
    u,v = orientation
    if (position, orientation) in edge_cases:
        next_position, next_orientation = edge_cases[(position, orientation)]
    else:
        next_position = (i+u, j+v)
        next_orientation = orientation
    if board[next_position[0]][next_position[1]] == '.':
        return next_position, next_orientation
    else:
        return position, orientation


def traverse_cube(board, starting_position, starting_orientation, instructions):
    board_rendered = [[char for char in line] for line in board]
    edge_cases = paste_cube_edges(board)
    current_position = starting_position
    current_orientation = starting_orientation
    i = 0
    while i < len(instructions):
        record_position_at(board_rendered, current_position, current_orientation)
        if instructions[i] in 'LR':
            current_orientation = turn(current_orientation, instructions[i])
            i += 1
        else: 
            j = min([k for k in range(i+1, len(instructions)) if instructions[k] in 'LR'], default = len(instructions))
            number_of_steps = int(instructions[i:j])
            for _ in range(number_of_steps):
                record_position_at(board_rendered, current_position, current_orientation)
                current_position, current_orientation = move_along_cube(board, current_position, current_orientation, edge_cases)
            i = j
    print('\n'.join([''.join(line) for line in board_rendered]))
    return current_position, current_orientation


starting_position = (0, min([j for j, char in enumerate(board[0]) if char == '.']))
starting_orientation = (0,1)

final_position, final_orientation = traverse_cube(board, starting_position, starting_orientation, instructions)

final_row = final_position[0] + 1
print('final row: ', final_row)
final_column = final_position[1] + 1
print('final column: ', final_column)
final_password = 1000*final_row + 4*final_column + direction_value[final_orientation]
print('final password: ', final_password)
