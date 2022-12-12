from string import ascii_lowercase

with open('./input12.txt') as f:
    data = f.read()
rows = data.split('\n')[:-1]

def bfs_walk_length(start, label, end_labels, directed_edges):
    visited = {start}
    current = [start]
    steps = 0
    seen_labels = set()
    while all([val not in seen_labels for val in end_labels]):
        new = set()
        while current:
            node = current.pop()
            for nbr in directed_edges[node]:
                if nbr not in visited:
                    new.add(nbr)
        visited |= new
        seen_labels |= {label[node] for node in new}
        current = [node for node in new]
        steps += 1
    return steps

m,n = len(rows), len(rows[0])
height = {'S': 0, 'E': 25} | {char: i for i,char in enumerate(ascii_lowercase)}
label = {(i,j): rows[i][j] for i in range(m) for j in range(n)}

# part 1
start = [(i,row.index('S')) for i,row in enumerate(rows) if 'S' in row][0]
directed_edges = {(x,y): [(x+i,y+j) for i,j in [(1,0), (0,1), (-1,0), (0,-1)]
                                    if (0 <= x+i < m and  
                                        0 <= y+j < n and  
                                        height[rows[x+i][y+j]] <= height[rows[x][y]] + 1)]
                  for x in range(m) for y in range(n)}
print(bfs_walk_length(start, label, ['E'], directed_edges))

# part 2
end = [(i,row.index('E')) for i,row in enumerate(rows) if 'E' in row][0]
directed_edges = {(x,y): [(x+i,y+j) for i,j in [(1,0), (0,1), (-1,0), (0,-1)]
                                    if (0 <= x+i < m and  
                                        0 <= y+j < n and  
                                        height[rows[x][y]] <= height[rows[x+i][y+j]] + 1)] 
                  for x in range(m) for y in range(n)}
print(bfs_walk_length(end, label, ['S', 'a'], directed_edges))
