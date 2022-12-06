with open('./input6.txt') as f:
    data = f.read()

# part 1
i = 0
while len(set(data[i:i+4])) != 4:
    i += 1
print(i+4)

# part 2
i = 0
while len(set(data[i:i+14])) != 14:
    i += 1
print(i+14)
