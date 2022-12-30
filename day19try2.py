import itertools
import collections
from time import process_time

with open('./input19.txt') as f:
    data = f.read()

datanot = '''Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
'''

blueprints = data.split('\n')[:-1]

def get_cost_dict(blueprint_string):
    words = blueprint_string.split(' ')
    cost = {m: collections.defaultdict(int) for m in 'rcbg'}
    cost['r']['r'] = int(words[6])
    cost['c']['r'] = int(words[12]) 
    cost['b']['r'] = int(words[18]) 
    cost['b']['c'] = int(words[21])
    cost['g']['r'] = int(words[27])
    cost['g']['b'] = int(words[30])
    return cost

def simulate(strategy, cost, max_time):
    i = 0
    res = {m: 0 for m in 'rcbg'}
    bot = {m: 0 for m in 'rcbg'}
    bot['r'] = 1
    for _ in range(max_time):
        build = False
        if i < len(strategy) and all([res[m] >= cost[strategy[i]][m] for m in 'rcbg']):
            build = True
        elif i >= len(strategy) and all([res[m] >= cost['g'][m] for m in 'rb']):
            build = True
        for m in 'rcbg':
            res[m] += bot[m]
        if build:
            bm = strategy[i] if i < len(strategy) else 'g'
            #print('building a {} bot'.format(bm))
            bot[bm] += 1
            for m, val in cost[bm].items():
                res[m] -= val
            i += 1
        #print(_+1, res)
    return res['g']

cost = get_cost_dict(blueprints[2])
print('my crazy', simulate('rrccccccbcbbbgbgb', cost, 32))


'''rrccccccbcbbbgbgb
r_r = 2
r_c = 6
c_c = 2
5 = n - 2 - r_r - r_c - c_c?
'''

# def iter_strategies_of_length(n):
#     return ( chunk_1 + ('c',) + chunk_2 + ('b',) + chunk_3 + ('b',)
#                 for c_1 in range(n - 3)
#                 for c_2 in range(n - 3 - c_1)
#                 for chunk_1 in itertools.product('rc', repeat=c_1)
#                 for chunk_2 in itertools.product('cb', repeat=c_2)
#                 for chunk_3 in itertools.product('bg', repeat=n - 3 - c_1 - c_2) )


# def iter_strategies_of_length(n):
#     return ( ('r',) + head + ('c',)*r_c + ('b',) + chunk_cbg + ('b',)
#                 for head in (('r','c','c'), ('c','r','c'), ('c','c','r'), ('r','r','c'), ('r','c','r'), ('c','c','r'))
#                 for r_c in range(3, n - 6)
#                 for chunk_cbg in itertools.product('cbg', repeat=n - 6 - r_c)
#                )

def iter_strategies_of_length(n):
    return ( ('r', 'r') + ('c',)*r_c + ('b',) + chunk_cb + chunk_bg + ('b',)
                for r_c in range(6, n - 4)
                for c_cb in range(n - 4 - r_c)
                for chunk_cb in itertools.product('cb', repeat=c_cb)
                for chunk_bg in itertools.product('bg', repeat=n - 4 - r_c - c_cb)
                )
                
# test = 'rcccccccbbbbgb'
# #test = 'rccccccccbbbgg'
# for item in iter_strategies_of_length(14): 
#     #print(''.join(item))
#     #if ''.join(item).startswith('rcccccccbc'):
#         #print(''.join(item))
#     if ''.join(item) == test:
#         print('found it')
# '''
# r + 6c + c + 4b+g 
# '''
def search_for_best_strategy(blueprint, min_strat_len, max_strat_len, max_time):
    cost = get_cost_dict(blueprint)
    print('Examining blueprint:'.format(cost))
    for m in 'rcbg':
        print('   ', m, '->', dict(cost[m]))
    strat_len = min_strat_len
    best = 20
    while strat_len < max_strat_len + 1:
        seen_ties = set()
        prev_time = process_time()
        for strat in iter_strategies_of_length(strat_len):
            value = simulate(strat, cost, max_time)
            if value > best:
                print('New best found: {} geodes with strategy {}'.format(
                    value, ''.join(strat)
                ))
                best = value
                seen_ties.add(strat)
            elif value == best and ''.join(strat) not in seen_ties:
                print('   tied with {}'.format(''.join(strat)))
                seen_ties.add(''.join(strat))
        print('Examining {} length strategies took {} sec'.format(
            strat_len, process_time()-prev_time))
        strat_len += 1
    return best

result = []
product = 1

for blueprint in blueprints[:3]:
    bp_val = search_for_best_strategy(blueprint, 17, 24, 32)
    result.append(bp_val)
    product *= bp_val

print(result)
print('final answer: {}'.format(product))

'''
attempt on 10, 19, 32
1. 20 geodes with strategy rrcccccccbccbcbbgb (length 19)
2. 24 geodes with strategy rrcccccccbbbbbgbb (length 18)
3. 38 geodes with strategy rrccccccbcbbbgbgb (length 18)
final answer 18240
attempt on 14, 20, 32 yields the same...

attempt on 21, 21, 32
1. 21 geodes with strategy rrcccccccbccbcbbgbgb (length 21)
2. 25 geodes with strategy rrcccccccbbcbcbbgbbb (length 21)
3. 37 geodes with strategy rccccbcbbgbgbgggbggb (length 21)
final answer 19425
but this missed the 38 strategy.
tried 19950 but it was also too low.

modified to require starting with chunk of consecutive 'r's and 'c's.

attempt on 17, 23, 32
1. 21 geodes with strategy rrcccccccbccbcbbgbgb (length 20)
2. 26 geodes with strategy rrcccccccbbcbcbbbgbbgb (length 22)
3. 38 geodes with strategy rrccccccbcbbbgbgb (length 17)
final answer 20748. 
no luck.

looking for inspiration, tried reverting to a more general iterator and displaying ties.
'''


