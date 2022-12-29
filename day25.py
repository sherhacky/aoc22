with open('./input25.txt') as f:
    data = f.read()

import itertools

datas = '''1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
'''
rows = data.split('\n')[:-1]

def snafu_to_decimal(snafu_string):
    value = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
    result = 0
    for i in range(len(snafu_string)):
        result += value[snafu_string[-1-i]]*5**i
    return result

for row in rows:
    print(row, snafu_to_decimal(row))



    # =  0  
    # -  1
    # 0  2
    # 1  3  
    # 2  4   

def decimal_to_base(n, b):
    if n == 0:
        return '0'
    result = []
    while n > 0:
#        print('m?', n)
        result.append(str(n % b))
        n //= b
#        print('n?', n)
    return ''.join(result[::-1])

print(decimal_to_base(537, 5))

def decimal_to_snafu(n):
    #print('looking at', n)
    if n in [1,2]:
        return str(n)
    cutpoints = [1]
    while cutpoints[-1] < n:
        cutpoints.append(cutpoints[-1] + 5**(len(cutpoints)//2))
        # print(cutpoints[-1])
    first_char = '1' if len(cutpoints) % 2 else '2'
    extra_space_count = len(cutpoints) // 2 - 1
#    print('looking at', n, cutpoints)
    remainder = n - max(p for p in cutpoints if p < n) - 1
    #print('rem', n, remainder)
    r_base_five = decimal_to_base(remainder, 5)
    #print('b5', r_base_five)
    val = {str(i): char for i, char in enumerate('=-012')}
    tentative = [val[d] for d in r_base_five]
    final = ['=' for _ in range(extra_space_count - len(tentative))] + tentative
    return ''.join([first_char] + final)



print(decimal_to_snafu(400))

    
for i in range(1,100):
    print(i, decimal_to_snafu(i))
i = 314159265
print(i, decimal_to_snafu(i))

test = '''1
2
1=
1-
10
11
12
2=
2-
20
21
22
1==
1=-
1=0
1=1
1=2
1-=
1--
1-0
1-1
1-2
20=
20-
200
201
202
21=
21-
210
211
212
22=
22-
220
221
222
1==='''

# for row in test.split('\n'):
#     print(row, ';', snafu_to_decimal(row))


# snafus = []
# for i in range(1,5):
#     for st in itertools.product('=-012', repeat=i):
#         snafus.append(''.join(st))

# print(snafus)
# snafus = sorted(snafus, key = lambda x: snafu_to_decimal(x))

# snafus = [st for st in snafus if st[0] != '0']

# for st in snafus:
#     print(snafu_to_decimal(st), st)

# print(decimal_to_base(149, 5))

# print(decimal_to_snafu(4890))

print(decimal_to_snafu(sum(snafu_to_decimal(row) for row in rows)))