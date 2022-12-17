from time import process_time
import itertools
import collections

with open('./input16.txt') as f:
    data = f.read()

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

distance = dict()
for start_node in ['AA'] + nonzero_nodes:
    distance[(start_node, start_node)] = 0
    current_nodes = {start_node}
    i = 0
    while any([node not in current_nodes for node in weight]):
        i += 1
        next_nodes = {v for node in current_nodes for v in neighbors[node] if v not in current_nodes}
        for node in next_nodes:
            distance[(start_node,node)] = i
        current_nodes |= next_nodes

def previous_states(state, node):
    result = []
    previous_state = list(state)
    previous_state[nonzero_nodes.index(node)] = 0
    previous_nodes = [nonzero_nodes[i] for i, val in enumerate(previous_state) if val]
    if not previous_nodes:
        previous_nodes.append('AA')
    for previous_node in previous_nodes:
        time_taken = distance[(node, previous_node)] + 1
        result.append((tuple(previous_state), previous_node, time_taken))
    return result

def best_values_at_state_dict(total_time):
    best_values = dict()
    best_values_at_state = collections.defaultdict(int)
    for state in itertools.product([0, 1], repeat=len(nonzero_nodes)):
        if not any(state):
            best_values[(state, 'AA')] = {0: 0}
            continue
        positions = [i for i, val in enumerate(state) if val]
        for i in positions:
            node = nonzero_nodes[i]
            best_values[(state, node)] = collections.defaultdict(int)
            for previous_state, previous_node, time_taken in previous_states(state, node):
                for t in best_values[(previous_state, previous_node)]:
                    if t + time_taken < total_time:
                        value_from_previous = best_values[(previous_state, previous_node)][t]
                        current_value = value_from_previous + (total_time - (t + time_taken)) * weight[node]
                        best_values[(state, node)][t + time_taken] = max(
                            current_value,
                            best_values[(state, node)][t + time_taken]
                        )
        best_values_at_state[state] = max([v for position in nonzero_nodes if (state, position) in best_values  \
                                             for v in best_values[(state, position)].values()],
                                          default=0)
    return best_values_at_state

# part 1
best_values_at_state = best_values_at_state_dict(30)
print('Part 1:', max(best_values_at_state.values()))
print(process_time(), 'seconds elapsed')

# part 2
def power_set(char_fun):
    if len(char_fun) == 0:
        return {tuple([])}
    return {(i,) + subset for i in range(char_fun[0] + 1) for subset in power_set(char_fun[1:])}

best_values_at_state = best_values_at_state_dict(26)
best = 0
for subset in itertools.product([0,1], repeat=len(nonzero_nodes)):
    complement = tuple(1-i for i in subset)
    for further_subset in power_set(subset):
        best = max(best, best_values_at_state[further_subset] + best_values_at_state[complement])

print('Part 2:', best)
print(process_time(), 'seconds elapsed')
