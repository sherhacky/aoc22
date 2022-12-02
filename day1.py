with open('./input1.txt') as f:
    data = f.read()

groups = data.split('\n\n')[:-1]

number_lists = [[int(item) for item in group.split('\n')] for group in groups]
sums = [sum(group) for group in number_lists]

sorted_sums = sorted(sums)

print(sorted_sums[-1])
print(sum(sorted_sums[-3:]))