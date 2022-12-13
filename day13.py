from functools import cmp_to_key

with open('./input13.txt') as f:
    data = f.read()

row_pairs = data[:-1].split('\n\n')
list_pairs = [[eval(item) for item in pair.split('\n')] for pair in row_pairs]

def compare(left, right):
    if type(left) == type(right) == list:
        if len(left) == len(right) == 0:
            return 'I'
        elif 0 in [len(left), len(right)]:
            return 'T' if len(left) == 0 else 'F'
        inner_compare = compare(left[0], right[0])
        if inner_compare == 'I':
            return compare(left[1:], right[1:])
        return inner_compare
    elif type(left) == type(right) == int:
        if left != right:
            return 'T' if left < right else 'F'
        return 'I'
    elif type(left) == int and type(right) == list:
        return compare([left], right)
    elif type(left) == list and type(right) == int:
        return compare(left, [right])

# part 1
total = 0
for i, [left, right] in enumerate(list_pairs):
    if compare(left, right) == 'T':
        total += i + 1
print(total)

# part 2
lists = [pair[i] for pair in list_pairs for i in range(2)] + [[[2]], [[6]]]

def comparison_function(left, right):
    result = compare(left, right)
    return ['T', 'I', 'F'].index(result) - 1

sorted_lists = sorted(lists, key=cmp_to_key(comparison_function))

print((sorted_lists.index([[2]]) + 1) * (sorted_lists.index([[6]]) + 1))
