with open('./input4.txt') as f:
    data = f.read()

rows = data.split('\n')[:-1]

# part 1

def symmetric_contains(a,b,x,y):
    return (a <= x and y <= b) or (x <= a and b <= y)

total = 0
for row in rows:
    [left, right] = row.split(',')
    [a,b] = left.split('-')
    [x,y] = right.split('-')
    total += int(symmetric_contains(int(a),int(b),int(x),int(y)))
print(total)

# part 2

def overlaps(a,b,x,y):
    return not(b<x or y<a)

total = 0
for row in rows:
    [left, right] = row.split(',')
    [a,b] = left.split('-')
    [x,y] = right.split('-')
    total += int(overlaps(int(a),int(b),int(x),int(y)))
print(total)
