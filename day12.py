from math import prod
import collections
import string

with open('./input12.txt') as f:
    data = f.read()

datas='''Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''

rows = data.split('\n')[:-1]

letters = string.ascii_lowercase
height = {**{'S': 0, 'E': 25}, **{char: i for i,char in enumerate(letters)}}
print(height)

for i,row in enumerate(rows):
    if 'S' in row:
        start = (i, row.index('S'))
    if 'E' in row:
        end = (i, row.index('E'))

m,n = len(rows), len(rows[0])

visited = {start}
next_group = {start}

steps = 0

while end not in visited:
    new = set()
    while next_group:
        x,y = next_group.pop()
        for i,j in [(1,0), (0,1), (-1,0), (0,-1)]:
            if 0 <= x+i < m and 0 <= y+j < n and height[rows[x+i][y+j]] <= height[rows[x][y]] + 1 and (x+i,y+j) not in visited:
                new.add((x+i,y+j))
    visited |= new
    next_group = {pt for pt in new}
    steps += 1

print(steps)

visited = {end}
next_group = {end}

steps = 0
seen_values = set()

while 0 not in seen_values:
    new = set()
    while next_group:
        x,y = next_group.pop()
        for i,j in [(1,0), (0,1), (-1,0), (0,-1)]:
            if 0 <= x+i < m and 0 <= y+j < n and height[rows[x][y]] <= height[rows[x+i][y+j]] + 1 and (x+i,y+j) not in visited:
                new.add((x+i,y+j))
    visited |= new
    seen_values |= {height[rows[i][j]] for i,j in new}
    next_group = {pt for pt in new}
    steps += 1

print(steps)