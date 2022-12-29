with open('./input23.txt') as f:
    data = f.read()


import collections

datas = '''..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............
'''

rows = data.split('\n')[:-1]

elf_spots = set()

for i, row in enumerate(rows):
    for j, char in enumerate(row):
        if char == '#':
            elf_spots.add((i,j))

elf_proposal = dict()

# for (i,j) in elf_spots:
#     if all ([(i-1, j-1), (i-1, j), (i-1, j+1) not in elf_spots]):
#         elf_proposal[(i,j)] = (i-1,j)
#     elif all ([(i+1, j-1), (i+1, j), (i+1, j+1) not in elf_spots]):
#         elf_proposal[(i,j)] = (i+1,j)
#     elif all ([(i-1, j-1), (i, j-1), (i+1, j-1) not in elf_spots]):
#         elf_proposal[(i,j)] = (i,j-1)
#     elif all ([(i-1, j+1), (i, j+1), (i+1, j+1) not in elf_spots]):
#         elf_proposal[(i,j)] = (i,j+1)
        
def consider_directions(i, j, dir_list):
    # print('considering', i, j)
    # print(elf_spots)
    # print({(i+a,j+b) for a in [-1,0,1] for b in [-1,0,1]})
    if len(elf_spots & {(i+a,j+b) for a in [-1,0,1] for b in [-1,0,1]}) == 1:
#        print('hmm', i, j)
        return None
    for orientation in dir_list:
#        print('looking at ', orientation)
        if orientation == (-1, 0) and all([p not in elf_spots for p in [(i-1, j-1), (i-1, j), (i-1, j+1)]]):
#            print('N')
            return (i-1,j)
        elif orientation == (1, 0) and all([p not in elf_spots for p in [(i+1, j-1), (i+1, j), (i+1, j+1)]]):
#            print('S')
            return (i+1,j)
        elif orientation == (0, -1) and all([p not in elf_spots for p in [(i-1, j-1), (i, j-1), (i+1, j-1)]]):
#            print('W')
            return (i,j-1)
        elif orientation == (0, 1) and all([p not in elf_spots for p in [(i-1, j+1), (i, j+1), (i+1, j+1)]]):
#            print('E')
            return (i,j+1)
    return None

dir_list = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def print_board(elf_spots):
    i_m, i_M = min(i for (i,j) in elf_spots), max(i for (i,j) in elf_spots)
    j_m, j_M = min(j for (i,j) in elf_spots), max(j for (i,j) in elf_spots)
    for i in range(i_m, i_M+1):
        row = []
        for j in range(j_m, j_M+1):
            row.append('#' if (i,j) in elf_spots else '.')
        print(''.join(row))



# part 2 



print_board(elf_spots)


for rnd in range(10):
    # print('dirs', dir_list)
    # print(elf_spots)
    # print('round: ', rnd)
    elf_proposal = dict()
    for (i,j) in elf_spots:
        proposal = consider_directions(i,j,dir_list)
        if proposal:
            # print('found', proposal)
            elf_proposal[(i,j)] = proposal
    proposal_count = collections.Counter(elf_proposal.values())
    # print('propose', elf_proposal )
    # print(proposal_count)
    for (i,j) in elf_proposal:
        if proposal_count[elf_proposal[(i,j)]] == 1:
            elf_spots.discard((i,j))
            elf_spots.add(elf_proposal[(i,j)])
    # print_board(elf_spots)
    dir_list.append(dir_list.pop(0))

def count_empty_spaces(elf_spots):
    i_m, i_M = min(i for (i,j) in elf_spots), max(i for (i,j) in elf_spots)
    j_m, j_M = min(j for (i,j) in elf_spots), max(j for (i,j) in elf_spots)
    return (i_M - i_m + 1)*(j_M - j_m + 1) - len(elf_spots)

print('final', count_empty_spaces(elf_spots))



# part 2
elf_spots = set()

for i, row in enumerate(rows):
    for j, char in enumerate(row):
        if char == '#':
            elf_spots.add((i,j))
dir_list = [(-1, 0), (1, 0), (0, -1), (0, 1)]

elf_proposal = dict()
moved = 1
rnd = 0
while moved > 0:
    rnd += 1
    moved = 0
    # print('dirs', dir_list)
    # print(elf_spots)
    if rnd % 100 == 0:
        print('round: ', rnd)
    elf_proposal = dict()
    for (i,j) in elf_spots:
        proposal = consider_directions(i,j,dir_list)
        if proposal:
            # print('found', proposal)
            elf_proposal[(i,j)] = proposal
    proposal_count = collections.Counter(elf_proposal.values())
    # print('propose', elf_proposal )
    # print(proposal_count)
    for (i,j) in elf_proposal:
        if proposal_count[elf_proposal[(i,j)]] == 1:
            moved += 1
            elf_spots.discard((i,j))
            elf_spots.add(elf_proposal[(i,j)])
    dir_list.append(dir_list.pop(0))


print('took ', rnd, 'rounds ')