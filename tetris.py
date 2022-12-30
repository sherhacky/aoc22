from pynput import keyboard
import time

width = 10
height = 16
tetrominos_string = rocks_string = '''####

.#.
###

.#
.#
##

#.
#.
##

#.
##
.#

.#
##
#.

##
##'''

class Gamestate():
    def __init__(self):
        self.current_piece = 'test'

        

tetrominos = []
for tetromino_string in tetrominos_string.split('\n\n'):
    tetromino = tetromino_string.split('\n')[::-1]
    tetromino_positions = [(i,j) for i in range(len(tetromino)) for j in range(len(tetromino[0])) if tetromino[i][j] == '#']
    tetrominos.append(tetromino_positions)

def shift_horiz(piece, char):
    shift = 1 if char == '>' else -1
    next_position = [(i, j+shift) for (i, j) in piece]
    if all([0 <= j < width for (i,j) in next_position]) \
           and all([i >= 0 and (i,j) not in occupied_positions for (i,j) in next_position]):
        return next_position
    return piece

def shift_down(piece):
    next_position = [(i-1, j) for (i, j) in piece]
    if all([i >= 0 and (i,j) not in occupied_positions for (i,j) in next_position]):
        return next_position
    return piece

def rotate(piece, char):
    center_i = max(i-1 for (i,j) in piece)
    center_j = min(j+1 for (i,j) in piece)
    shifted = [(i - center_i, j - center_j) for (i,j) in piece]
    if char == 'l':
        rotated = [(-j, i) for (i,j) in shifted]
    else:
        rotated = [(i, -j) for (i,j) in shifted]
    next_position = [(i + center_i, j + center_j) for (i,j) in rotated]
    if all([0 <= j < width for (i,j) in next_position]) \
           and all([i >= 0 and (i,j) not in occupied_positions for (i,j) in next_position]):
        return next_position
    return piece

def seed_tetromino(piece):
    return [(height + i, width//2 - 1 + j) for (i, j) in piece]

def print_board(tetromino, occupied_positions):
    print('\n'.join(board_string(tetromino, occupied_positions)))

def board_string(tetromino, occupied_positions):
    result = []
    board = [['.' for j in range(width)] for i in range(height)]
    for (i,j) in tetromino:
        if 0 <= i < height and 0 <= j < width:
            board[i][j] = '@'
    for (i,j) in occupied_positions:
        if 0 <= i < height and 0 <= j < width:
            board[i][j] = '#'
    for row in board[::-1]:
        result.append(('|' + ''.join(row) + '|'))
    result.append('+' + '-'*width + '+')
    return tuple(result)

move_queue = []
def on_press(key):
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k == 'left':
        move_queue.append('<')
    if k == 'right':
        move_queue.append('>')
    if k == 'z':
        move_queue.append('l')
    if k == 'x':
        move_queue.append('r')

def check_and_clear(occupied_positions):
    for i in range(height):
        if all([(i,j) in occupied_positions for j in range(width)]):
            occupied_positions -= set([(i,j) for j in range(width)])
            shift_down = {(k-1, j) for (k,j) in occupied_positions if k > i}
            for k in range(i + 1, height):
                occupied_positions -= set([(k,j) for j in range(width)])
            occupied_positions |= shift_down
            return

i_t = 0
listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread
#listener.join()  # remove if main thread is polling self.keys
increment = 0.2
previous_down = 0
occupied_positions = set()
while True:
    piece = seed_tetromino(tetrominos[i_t])
    print_board(piece, occupied_positions)
    falling = True
    while falling:
        if move_queue:
            char = move_queue.pop()
            if char in '<>':
                piece = shift_horiz(piece, char)
            if char in 'lr':
                piece = rotate(piece, char)
            print_board(piece, occupied_positions)
        if time.time() - previous_down > increment:
            print(time.time() - previous_down)
            next_position = shift_down(piece)
            if next_position == piece:
                falling = False
            else:
                piece = next_position
            print_board(piece, occupied_positions)
            previous_down = time.time()    
    occupied_positions |= set(piece)
    check_and_clear(occupied_positions)
    i_t = (i_t + 1) % len(tetrominos)
