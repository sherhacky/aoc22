import time
import itertools

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
print(weight)
print(neighbors)

'''dp idea: for each vertex v and time t, 
dp[(v,t)] is the max releaseable from that point if it's opened at time -t.
simple recursion.  
However there are many possible configurations of open valves...
so I guess that's the thing: power set of valves'''

states = [st for st in itertools.product([0,1], repeat=len(nonzero_nodes))]

def pressure_release(state):
    return sum(weight[node] for i, node in enumerate(nonzero_nodes) if state[i])

def open_at(state, position):
    if weight[position] == 0:
        return state
    else:
        i = nonzero_nodes.index(position)
        result_state = list(state)
        result_state[i] = 1
        return tuple(result_state)


print([(state, pressure_release(state)) for state in states[:5]])
best_values = {(state, position): pressure_release(state) for state in states for position in weight}
print(max(best_values.values()))
for _ in range(29):
    new_best_values = dict()
    for (state, position) in best_values:
        new_best_values[(state, position)] = pressure_release(state) + max([
            best_values[(state, node)] for node in neighbors[position]
        ] + [
            best_values[(open_at(state, position), position)]
        ])
    best_values = new_best_values

print(_, best_values[((0,)*len(nonzero_nodes), 'AA')])
print('part 1 took ', time.process_time(), 'seconds')
# part 2... naive

best_values = {(state, position1, position2): pressure_release(state) for state in states for position1 in weight \
                for position2 in weight}

def neighbor_states(state, position1, position2):
    result = []
    # position 1 opens, 2 stands still or moves
    for node2 in neighbors[position2]:
        result.append((open_at(state, position1), position1, node2))
    # reverse
    for node1 in neighbors[position1]:
        result.append((open_at(state, position2), node1, position2))
    # both move?
        for node2 in neighbors[position2]:
            result.append((state, node1, node2))
    # both open?
    result.append((open_at(open_at(state, position1), position2), position1, position2))
    return result


for iteration in range(25):
    new_best_values = dict()
    for (state, position1, position2) in best_values:
        new_best_values[(state, position1, position2)] = pressure_release(state) + max(
            best_values[neighbor] for neighbor in neighbor_states(state, position1, position2)
        )
    print('iteration', str(iteration), ':', time.process_time())
    best_values = new_best_values

print(_, best_values[((0,)*len(nonzero_nodes), 'AA', 'AA')])

distance = dict()
for start_node in weight:
    distance[(start_node,start_node)] = 0
    current_nodes = {start_node}
    i = 0
    while any([node not in current_nodes for node in weight]):
        i += 1
        next_nodes = {v for node in current_nodes for v in neighbors[node] if v not in current_nodes}
        for node in next_nodes:
            distance[(start_node,node)] = i
        current_nodes |= next_nodes

for node1 in nonzero_nodes:
    print([(node1, node2, distance[(node1, node2)]) for node2 in nonzero_nodes])

reachable_states = [set() for _ in range(27)]
current_states = {((0,)*len(nonzero_nodes), 'AA', 'AA')}