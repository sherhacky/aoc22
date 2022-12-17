from time import process_time
import itertools
import collections

with open('./input17.txt') as f:
    data = f.read()

shifts = data.split('\n')[:-1][0]

shifts = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'

rocks_string = '''####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##'''

rocks = []
for rock_string in rocks_string.split('\n\n'):
    rock = rock_string.split('\n')[::-1]
    rock_positions = [(i,j) for i in range(len(rock)) for j in range(len(rock[0])) if rock[i][j] == '#']
    rocks.append(rock_positions)

print(rocks)

def shift_horiz(rock, char):
    shift = 1 if char == '>' else -1
    return [(i, j+shift) for (i, j) in rock]

def shift_down(rock):
    return [(i-1, j) for (i, j) in rock]

def seed_rock(rock, max_vertical):
    return [(max_vertical + i + 3, j + 2) for (i, j) in rock]

def print_board(rock, occupied_positions):
    # m = max(i + 1 for i,j in occupied_positions | set(rock))
    # board = [['.' for j in range(7)] for i in range(m)]
    # for (i,j) in rock:
    #     board[i][j] = '@'
    # for (i,j) in occupied_positions:
    #     board[i][j] = '#'
    # #print(board)
    # for row in board[-1:-20:-1]:
    #     print('|' + ''.join(row) + '|')
    # print('+' + '-'*7 + '+')
    print('\n'.join(clipped_board(rock, occupied_positions)))

def clipped_board(rock, occupied_positions):
    result = []
    m = max(i + 1 for i,j in occupied_positions | set(rock))
    board = [['.' for j in range(7)] for i in range(m)]
    for (i,j) in rock:
        board[i][j] = '@'
    for (i,j) in occupied_positions:
        board[i][j] = '#'
    #print(board)
    for row in board[-1:-20:-1]:
        result.append(('|' + ''.join(row) + '|'))
    result.append('+' + '-'*7 + '+')
    return tuple(result)

def simulate_dropped_rocks(num_rocks):
    print('Dropping {} rocks yields:'.format(num_rocks))
    i_shift = 0
    i_rock = 0
    stack_height = 0
    occupied_positions = set()
    for _ in range(num_rocks):
        rock = seed_rock(rocks[i_rock], stack_height)
    #    print('stack height is ', stack_height)
        resting = False
        while not resting:
        #    print(rock)
            #print_board(rock, occupied_positions)
            next_position = shift_horiz(rock, shifts[i_shift])
            if all([0 <= j < 7 for (i,j) in next_position]) and all([i >= 0 and (i,j) not in occupied_positions for (i,j) in next_position]):
                rock = next_position
            #print_board(rock, occupied_positions)
            next_position = shift_down(rock)
            if all([i >= 0 and (i,j) not in occupied_positions for (i,j) in next_position]):
                rock = next_position
            else:
                resting = True
                occupied_positions |= set(rock)
                stack_height = max([i+1 for (i,j) in rock] + [stack_height])
            i_shift = (i_shift + 1) % len(shifts)
        i_rock = (i_rock + 1) % len(rocks)
    print_board(seed_rock(rocks[i_rock], stack_height), occupied_positions)
    print('Tower height:', stack_height)

simulate_dropped_rocks(2022)

i_shift = 0
i_rock = 0
stack_height = 0
occupied_positions = set()
seen_arrangements = dict()
board = clipped_board(rocks[0], occupied_positions)
rock_count = 0
heights = {0: 0}
while (board, i_shift, i_rock) not in seen_arrangements:
#for _ in range(5000):
    seen_arrangements[(board, i_shift, i_rock)] = [rock_count, stack_height]
    rock = seed_rock(rocks[i_rock], stack_height)
    # if rock_count % (1829 - 84) == 84:
    #     print_board(rock, occupied_positions)
    #     print(rock_count, i_shift, i_rock)
    #     print('stack height is ', stack_height)
    resting = False
    while not resting:
    #    print(rock)
        next_position = shift_horiz(rock, shifts[i_shift])
        if all([0 <= j < 7 for (i,j) in next_position]) and all([i >= 0 and (i,j) not in occupied_positions for (i,j) in next_position]):
            rock = next_position
        #print_board(rock, occupied_positions)
        next_position = shift_down(rock)
        if all([i >= 0 and (i,j) not in occupied_positions for (i,j) in next_position]):
            rock = next_position
        else:
            resting = True
            occupied_positions |= set(rock)
            stack_height = max([i+1 for (i,j) in rock] + [stack_height])
        i_shift = (i_shift + 1) % len(shifts)
    i_rock = (i_rock + 1) % len(rocks)
    board = clipped_board(rock, occupied_positions)
    rock_count += 1
    heights[rock_count] = stack_height

print('first loop encountered looks like:')
print_board(seed_rock(rocks[i_rock], stack_height), occupied_positions)
print('first phase: ', rock_count)
first_count, first_height = seen_arrangements[(board, i_shift, i_rock)]
print('seen at: ', first_count)
rock_period = rock_count - first_count
height_increase = stack_height - first_height

#many_rocks = 1000000000000
many_rocks = 33333
loops = many_rocks//rock_period

print('residues')
start_at = many_rocks
print(first_count)
while start_at % rock_period != first_count:
    start_at -= 1
print(many_rocks)
print(start_at)

simulate_dropped_rocks(first_count + many_rocks - start_at)

print('last_stack', stack_height)
print('first stack', first_height)
print('increase per loop', height_increase)
print('rocks first loop', first_count)
print('rocks per loop', rock_period)
print('total loops before big number', loops)
print(stack_height + loops*height_increase - first_height)
print(first_height + loops*height_increase + (stack_height - first_height))

'''print_board(seed_rock(rocks[i_rock], stack_height), occupied_positions)
print(stack_height)

rock_count = 1000000000000
while rock_count % 1745 != 84:
    rock_count -= 1

print(rock_count)
print(1000000000000 - rock_count)
print(1000000000000//1745)
print(rock_count//1745)
print(2738*(rock_count//1745))

'''
i_shift = 0
i_rock = 0
stack_height = 0
occupied_positions = set()

simulate_dropped_rocks(many_rocks)
simulate_dropped_rocks(start_at - 1)

# print(many_rocks)

# for _ in range(many_rocks):
#     rock = seed_rock(rocks[i_rock], stack_height)
# #    print('stack height is ', stack_height)
#     resting = False
#     while not resting:
#     #    print(rock)
#         #print_board(rock, occupied_positions)
#         next_position = shift_horiz(rock, shifts[i_shift])
#         if all([0 <= j < 7 for (i,j) in next_position]) and all([i >= 0 and (i,j) not in occupied_positions for (i,j) in next_position]):
#             rock = next_position
#         #print_board(rock, occupied_positions)
#         next_position = shift_down(rock)
#         if all([i >= 0 and (i,j) not in occupied_positions for (i,j) in next_position]):
#             rock = next_position
#         else:
#             resting = True
#             occupied_positions |= set(rock)
#             stack_height = max([i+1 for (i,j) in rock] + [stack_height])
#         i_shift = (i_shift + 1) % len(shifts)
#     i_rock = (i_rock + 1) % len(rocks)
# print_board(seed_rock(rocks[i_rock], stack_height), occupied_positions)
# print('height', stack_height)

# i_shift = 0
# i_rock = 0
# stack_height = 0
# occupied_positions = set()

# print(start_at)

# for _ in range(start_at-1):
#     rock = seed_rock(rocks[i_rock], stack_height)
# #    print('stack height is ', stack_height)
#     resting = False
#     while not resting:
#     #    print(rock)
#         #print_board(rock, occupied_positions)
#         next_position = shift_horiz(rock, shifts[i_shift])
#         if all([0 <= j < 7 for (i,j) in next_position]) and all([i >= 0 and (i,j) not in occupied_positions for (i,j) in next_position]):
#             rock = next_position
#         #print_board(rock, occupied_positions)
#         next_position = shift_down(rock)
#         if all([i >= 0 and (i,j) not in occupied_positions for (i,j) in next_position]):
#             rock = next_position
#         else:
#             resting = True
#             occupied_positions |= set(rock)
#             stack_height = max([i+1 for (i,j) in rock] + [stack_height])
#         i_shift = (i_shift + 1) % len(shifts)
#     i_rock = (i_rock + 1) % len(rocks)
# print_board(seed_rock(rocks[i_rock], stack_height), occupied_positions)
# print('height', stack_height)