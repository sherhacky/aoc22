from time import process_time
from sympy.solvers import solve
from sympy import Symbol

with open('./input20.txt') as f:
    data = f.read()

datas = '''1
2
-3
3
-2
0
4
'''

rows = data.split('\n')[:-1]


# print(len(rows))
# print(len(set(rows)))

num_list = [int(n) for n in rows]
handled = [False for n in rows]
modulus = len(num_list) - 1



def mix(num_list):
    i = 0
    while i < len(num_list):
        #print(i, num_list)
        if handled[i]:
            i += 1
        else:
            num = num_list.pop(i)
            handled.pop(i)
            new_position = (i + num) % modulus
            if new_position == 0:
                num_list.append(num)
                handled.append(True)
            else:
                num_list.insert(new_position, num)
                handled.insert(new_position, True)
            if new_position < i:
                i += 1
    return num_list

def sum_coordinates(num_list):
    return sum([num_list[(num_list.index(0) + k * 1000) % len(num_list)] for k in range(1,4)])

print(sum_coordinates(mix(num_list)))

decryption_key = 811589153
new_num_list = [decryption_key * int(num) for num in rows]

for _ in range(10):
    new_num_list = mix(new_num_list)

def mix(num_list, index_locations):
    for i in range(len(index_locations)):
        num = num_list.pop(i)
        new_position = (i + num) % modulus
        if new_position == 0:
            num_list.append(num)
        else:
            num_list.insert(new_position, num)
            handled.insert(new_position, True)

print(sum_coordinates(new_num_list))

new_num_list = [[k, decryption_key * int(num)] for k, num in enumerate(rows)]




def new_mix(num_list):
    for n in range(len(num_list)):
        i = 0
        while num_list[i][0] != n:
            i += 1
        [k, num] = num_list.pop(i)
        new_position = (i + num) % modulus
        if new_position == 0:
            num_list.append([k, num])
        else:
            num_list.insert(new_position, [k, num])
    return num_list

#new_num_list = [[k, int(num)] for k,num in enumerate(rows)]
for _ in range(10):
    new_num_list = new_mix(new_num_list)

print(sum_coordinates([t[1] for t in new_num_list]))
