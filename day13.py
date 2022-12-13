from string import ascii_lowercase
from functools import cmp_to_key

with open('./input13.txt') as f:
    data = f.read()
datas = '''[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''
row_pairs = data[:-1].split('\n\n')

print(row_pairs)

list_pairs = [[eval(item) for item in pair.split('\n')] for pair in row_pairs]
print(list_pairs)

def compare(left, right):
    if type(left) == type(right) == list:
        if len(left) == len(right) == 0:
            return 'I'
        elif 0 in [len(left), len(right)]:
            return 'T' if len(left) == 0 else 'F'
        else:
            inner_compare = compare(left[0], right[0])
            if inner_compare == 'I':
                return compare(left[1:], right[1:])
            else:
                return inner_compare
    elif type(left) == type(right) == int:
        if left != right:
            return 'T' if left < right else 'F'
        else:
            return 'I'
    elif type(left) == int and type(right) == list:
        return compare([left], right)
    elif type(left) == list and type(right) == int:
        return compare(left, [right])

total = 0
for i, [left, right] in enumerate(list_pairs):
    print(left)
    print(right)
    print(compare(left, right))
    if compare(left, right) == 'T':
        total += i + 1

print(total)

lists = [pair[i] for pair in list_pairs for i in range(2)] + [[[2]], [[6]]]

def comp_lists_boolean(left, right):
    result = compare(left, right)
    return ['T', 'I', 'F'].index(result) - 1

sorted_lists = sorted(lists, key=cmp_to_key(comp_lists_boolean))

for thing in sorted_lists:
    print(thing)

print((sorted_lists.index([[2]]) + 1) * (sorted_lists.index([[6]]) + 1))