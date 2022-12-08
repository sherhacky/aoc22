with open('./input8.txt') as f:
    data = f.read()
rows = data.split('\n')[:-1]

# part 1
def check(i,j):
    return any([
        all(rows[x][j] < rows[i][j] for x in range(i)),
        all(rows[x][j] < rows[i][j] for x in range(i+1,len(rows))),
        all(rows[i][y] < rows[i][j] for y in range(j)), 
        all(rows[i][y] < rows[i][j] for y in range(j+1,len(rows[0])))
        ])

print(sum(int(check(i,j)) for i in range(len(rows)) for j in range(len(rows[0]))))

# part 2
def viewing_score(x,y):
    prod = 1
    for (i,j) in [(0,1), (1,0), (-1,0), (0,-1)]:
        a, b = 0, 0
        while all([0 <= x+(a+i) < len(rows), 
                   0 <= y+(b+j) < len(rows[0]),
                   rows[x+a][y] < rows[x][y] or a == 0,
                   rows[x][y+b] < rows[x][y] or b == 0]):
            a += i
            b += j
        prod *= max(a,-a,b,-b)
    return prod

print(max(viewing_score(i,j) for i in range(len(rows)) for j in range(len(rows[0]))))
