with open('./input17.txt') as f:
    data = f.read()

shifts = data.split('\n')[:-1][0]

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

def shift_horiz(rock, char):
    shift = 1 if char == '>' else -1
    return [(i, j+shift) for (i, j) in rock]

def shift_down(rock):
    return [(i-1, j) for (i, j) in rock]

def seed_rock(rock, max_vertical):
    return [(max_vertical + i + 3, j + 2) for (i, j) in rock]

def print_board(rock, occupied_positions):
    print('\n'.join(clipped_board(rock, occupied_positions)))

def clipped_board(rock, occupied_positions):
    result = []
    m = max(i + 1 for i,j in occupied_positions | set(rock))
    board = [['.' for j in range(7)] for i in range(m)]
    for (i,j) in rock:
        board[i][j] = '@'
    for (i,j) in occupied_positions:
        board[i][j] = '#'
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
        resting = False
        while not resting:
            next_position = shift_horiz(rock, shifts[i_shift])
            if all([0 <= j < 7 for (i,j) in next_position]) \
               and all([i >= 0 and (i,j) not in occupied_positions for (i,j) in next_position]):
                rock = next_position
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
    return stack_height

# part 1
simulate_dropped_rocks(2022)

# part 2
i_shift = 0
i_rock = 0
stack_height = 0
occupied_positions = set()
seen_arrangements = dict()
board = clipped_board(rocks[0], occupied_positions)
rock_count = 0
while (board, i_shift, i_rock) not in seen_arrangements:
    seen_arrangements[(board, i_shift, i_rock)] = [rock_count, stack_height]
    rock = seed_rock(rocks[i_rock], stack_height)
    resting = False
    while not resting:
        next_position = shift_horiz(rock, shifts[i_shift])
        if all([0 <= j < 7 for (i,j) in next_position]) \
           and all([i >= 0 and (i,j) not in occupied_positions for (i,j) in next_position]):
            rock = next_position
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

[ct_0, ht_0] = seen_arrangements[(board, i_shift, i_rock)]
ct, ht = rock_count, stack_height
ct_delta, ht_delta = ct - ct_0, ht - ht_0

big_number = 1000000000000
ct_last_cycle = big_number
while ct_last_cycle % ct_delta != ct_0:
    ct_last_cycle -= 1

final_height = ht_delta * (ct_last_cycle // ct_delta) + simulate_dropped_rocks(ct_0 + big_number - ct_last_cycle)
print('After {} blocks are dropped, the tower will be height {}.'.format(big_number, final_height))
