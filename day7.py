import collections

with open('./input7.txt') as f:
    data = f.read()
rows = data.split('\n')[:-1]

stack = []
filepaths = dict()

# Using the dir tree walk, construct a dict of filepaths->sizes
i = 0
while i < len(rows):
    chunks = rows[i].split(' ')
    if chunks[0] == '$' and chunks[1] == 'cd':
        if chunks[2] == '..':
            stack.pop()
        else:
            stack.append(chunks[2])
        i +=1 
    elif chunks[0] == '$' and chunks[1] == 'ls':
        i += 1
        while i < len(rows) and rows[i][0] != '$':
            chunks = rows[i].split(' ')
            if chunks[0] != 'dir':
                stack.append(chunks[1])
                filepaths['/'.join(stack)] = int(chunks[0])
                stack.pop()
            i += 1

dir_sizes = collections.defaultdict(int)

# iterate through filepath sizes to determine directory sizes
for item in filepaths:
    subdirs = item.split('/')[1:]
    for i in range(1, len(subdirs)):
        dir_sizes['/'.join(subdirs[:i])] += filepaths[item]

# part 1
print(sum(size for size in dir_sizes.values() if size <= 100000))

# part 2
min_size_needed = dir_sizes[''] + 30000000 - 70000000
print(min(size for size in dir_sizes.values() if size > min_size_needed))
