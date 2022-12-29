from time import process_time
from sympy.solvers import solve
from sympy import Symbol

with open('./input21.txt') as f:
    data = f.read()



datas = '''root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
'''
rows = data.split('\n')[:-1]
monkey_strings = dict()
for row in rows:
    monkey_strings[row[:4]] = row[6:]

monkey_dict = dict()
def fill_in(monkey):
    if monkey in monkey_dict:
        return monkey_dict[monkey]
    elif monkey_strings[monkey][0] in '0123456789':
        monkey_dict[monkey] = int(monkey_strings[monkey])
        return monkey_dict[monkey]
    monkey_1 = monkey_strings[monkey][:4]
    monkey_2 = monkey_strings[monkey][-4:]
    monkey_dict[monkey] = eval(monkey_strings[monkey], {monkey_1: fill_in(monkey_1), monkey_2: fill_in(monkey_2)})
    return monkey_dict[monkey]


print(fill_in('root'))
    
# i = 0
# toggle = 0
# monkey_strings['root'] = monkey_strings['root'][:4] + '==' + monkey_strings['root'][-4:]
# monkey_dict['root'] = False
# while not monkey_dict['root']:
#     i += 1
#     monkey_dict = dict()
#     monkey_strings['humn'] = str(i)
#     fill_in('root')
#     # if toggle:
#     #     i *= -1
#     #     i += 1
#     # else:
#     #     i *= -1
#     # toggle = 1-toggle
#     if not i % 100000:
#         print('i = {} and still looking after {}sec'.format(i, process_time()))


equation = 'x + 10 - 4'
test = eval(equation, {'x': Symbol('x')})
print(test)
print(solve(test, Symbol('x')))

monkey_strings['root'] = monkey_strings['root'][:4] + '==' + monkey_strings['root'][-4:]
monkey_dict = {'humn': 'x'}
def expand(monkey):
    if monkey in monkey_dict:
        return monkey_dict[monkey]
    elif monkey_strings[monkey][0] in '0123456789':
        monkey_dict[monkey] = monkey_strings[monkey]
        return monkey_dict[monkey]
    monkey_1 = monkey_strings[monkey][:4]
    monkey_2 = monkey_strings[monkey][-4:]
    opn = monkey_strings[monkey][5]
    monkey_dict[monkey] = '({} {} {})'.format(expand(monkey_1), opn, expand(monkey_2))
    return monkey_dict[monkey]

x = Symbol('x')
equation = expand('root')
[left, right] = equation.split('=')
expression = left + '-' + right
print(solve(eval(expression, {'x': x}), x))