from time import process_time
import itertools
import collections

with open('./input16.txt') as f:
    data = f.read()

data='''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''

rows = data.split('\n')[:-1]

weight = dict()
neighbors = dict()
nonzero_nodes = []
for line in rows:
    words = line.split(' ')
    weight[words[1]] = int(words[4][5:-1])
    if weight[words[1]] > 0:
        nonzero_nodes.append(words[1])
    neighbors[words[1]] = [w[:2] for w in words[9:]]






def link_all_nonzero(node):
    pass

def pressure_release(state):
    return sum(weight[node] for i, node in enumerate(nonzero_nodes) if state[i]=='1')

def open_at(state, position):
    i = nonzero_nodes.index(position)
    result_state = list(state)
    result_state[i] = '1'
    return ''.join(result_state)

def close_at(state, position):
    i = nonzero_nodes.index(position)
    result_state = list(state)
    result_state[i] = '0'
    return ''.join(result_state)

valve_states = [''.join(st) for st in itertools.product('01', repeat=len(nonzero_nodes))]
states = {tup: 0 for tup in itertools.product(range(31), valve_states, nonzero_nodes)}
# print(states)

distance = dict()
for start_node in ['AA']+nonzero_nodes:
    distance[(start_node,start_node)] = 0
    current_nodes = {start_node}
    i = 0
    while any([node not in current_nodes for node in weight]):
        i += 1
        next_nodes = {v for node in current_nodes for v in neighbors[node] if v not in current_nodes}
        for node in next_nodes:
            distance[(start_node,node)] = i
        current_nodes |= next_nodes
print(max(distance.values()))
print(process_time())

def compute_path_value(node_list):
    time_passed = 1
    node_list = ('AA',) + node_list
    value = 0
    i = 1
    while i < len(node_list) and time_passed < 30:
        next_time = min(30, time_passed + distance[(node_list[i-1], node_list[i])])
        value += (next_time - time_passed)*sum(weight[node] for node in node_list[:i])
        i += 1
    return value

current_best = 0
for ordering in itertools.permutations(nonzero_nodes):
    value = compute_path_value(ordering)
    if value > current_best:
        print(ordering, value)
        current_best = value
        

def possible_next_states(time, state, position):
    result = []
    # open at current position
    result.append((time+1, open_at(state, position), position))
    # move 
    for next_node in nonzero_nodes:
        result.append((time+distance[(next_node, position)], state, next_node))
    return result

def possible_previous_states(time, state, position):
    result = []
    if time <= 0:
        return set()
    # just opened at current position
    result.append((time-1, close_at(state, position), position))
    # moved
    for next_node in nonzero_nodes:
        new_time = time-distance[(next_node, position)]
        if new_time >= 0:
            result.append((time-distance[(next_node, position)], state, next_node))
    return set(result)

best_values = collections.defaultdict(int)
# for position in nonzero_nodes:
#     best_values[(30, '1'*len(nonzero_nodes), position)] = 0
min_then = float('inf')
#while new_best_values:
for time in range(29, -1, -1):
    print('main loop:', time, process_time())
    for state, position in itertools.product(valve_states, nonzero_nodes):
        next_states = [(new_time, new_state, new_position) for new_time, new_state, new_position in \
            possible_next_states(time, state, position) if new_time <= 30]
        best_values[(time, state, position)] = max(
            (new_time - time)*pressure_release(state) + best_values[(new_time, new_state, new_position)] \
            for (new_time, new_state, new_position) in next_states
        )

    # possible_previous = set()
    # best_values |= new_best_values
    # for time, state, position in new_best_values:
    #     possible_previous |= possible_previous_states(time, state, position)
    # new_best_values = collections.defaultdict(int)
    # for time, state, position in possible_previous:
    #     for new_time, new_state, new_position in possible_next_states(time, state, position):
    #         if (new_time, new_state, new_position) in best_values:
    #             new_best_values[(time, state, position)] = max(
    #                 new_best_values[(time, state, position)],
    #                 ]
    #             )
    # min_now = min(time for time, state, position in new_best_values)
    # max_at_min = max([item for item in new_best_values.items() if item[0][0]==min_now], key=lambda item: item[1])
    # if min_now < min_then:
    #     min_then = min_now
    #     print(process_time(), min_then, max_at_min)
    # if (0, '0'*len(nonzero_nodes), 'AA') in best_values:
    #     print(i, best_values[(0, '0'*len(nonzero_nodes), 'AA')])
#    print(best_values)

# for node in nonzero_nodes:
#     if (1, '0'*len())
print(best_values[(0, '0'*len(nonzero_nodes), 'AA')])
print(process_time())