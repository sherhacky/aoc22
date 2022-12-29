import itertools
import collections
from time import process_time

with open('./input19.txt') as f:
    data = f.read()

data = '''Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
'''

rows = data.split('\n')[:-1]

def possible_next_values(configuration):
    minute, ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian, geode = configuration
    if ore < min([cost['ore'], cost['clay'], cost['obsidian'][0], cost['geode'][1]]):
        return [(minute + 1, ore_robots, clay_robots, obsidian_robots, geode_robots, 
                 ore + ore_robots, clay + clay_robots, obsidian + obsidian_robots, geode + geode_robots)]
    if ore >= cost['geode'][0] and obsidian >= cost['geode'][1]:
        return [(minute + 1, ore_robots, clay_robots, obsidian_robots, geode_robots + 1, 
                ore + ore_robots - cost['geode'][0], clay + clay_robots, obsidian + obsidian_robots - cost['geode'][1], geode + geode_robots)]
    if ore >= cost['obsidian'][0] and clay >= cost['obsidian'][1] and obsidian_robots == 0:
        return [(minute + 1, ore_robots, clay_robots, obsidian_robots + 1, geode_robots, 
                ore + ore_robots - cost['obsidian'][0], clay + clay_robots - cost['obsidian'][1], obsidian + obsidian_robots, geode + geode_robots)]
    result = [(minute + 1, ore_robots, clay_robots, obsidian_robots, geode_robots, 
                ore + ore_robots, clay + clay_robots, obsidian + obsidian_robots, geode + geode_robots)]
    if ore >= cost['obsidian'][0] and clay >= cost['obsidian'][1]:
        result.append((minute + 1, ore_robots, clay_robots, obsidian_robots + 1, geode_robots, 
                ore + ore_robots - cost['obsidian'][0], clay + clay_robots - cost['obsidian'][1], obsidian + obsidian_robots, geode + geode_robots))
    if ore >= cost['ore']:
        result.append((minute + 1, ore_robots + 1, clay_robots, obsidian_robots, geode_robots, 
                ore + ore_robots - cost['ore'], clay + clay_robots, obsidian + obsidian_robots, geode + geode_robots))
    if ore >= cost['clay']:
        result.append((minute + 1, ore_robots, clay_robots + 1, obsidian_robots, geode_robots, 
                ore + ore_robots - cost['clay'], clay + clay_robots, obsidian + obsidian_robots, geode + geode_robots))
    return result

most_geodes_obtainable = dict()

max_minutes = 24

def fill_in(configuration):
    if configuration[0] == max_minutes:
        return configuration[-1]
    elif configuration in most_geodes_obtainable:
        return most_geodes_obtainable[configuration]
    else:
        most_geodes_obtainable[configuration] = max(fill_in(new_configuration) for new_configuration in possible_next_values(configuration))
        return most_geodes_obtainable[configuration]

final_result = 0
for i, line in enumerate(rows):
    most_geodes_obtainable = dict()
    prev_time = process_time()
    blueprint_id = i + 1
    words = line.split(' ')
    cost = {'ore': int(words[6]), 
            'clay': int(words[12]), 
            'obsidian': (int(words[18]), int(words[21])), 
            'geode': (int(words[27]), int(words[30]))}
    print('Blueprint {}: {}'.format(blueprint_id, cost))
    max_geodes = fill_in((0, 1, 0, 0, 0, 0, 0, 0, 0))
    print(max_geodes, 'geode{} obtainable'.format('s'*int(max_geodes!=1)))
    print('Took', process_time() - prev_time, 'sec')
    final_result += blueprint_id * max_geodes

print('Final answer obtained in {} seconds:'.format(process_time()))
print(final_result)

# part 2
max_minutes = 32

for i, line in enumerate(rows):
    most_geodes_obtainable = dict()
    prev_time = process_time()
    blueprint_id = i + 1
    words = line.split(' ')
    cost = {'ore': int(words[6]), 
            'clay': int(words[12]), 
            'obsidian': (int(words[18]), int(words[21])), 
            'geode': (int(words[27]), int(words[30]))}
    print('Blueprint {}: {}'.format(blueprint_id, cost))
    max_geodes = fill_in((0, 1, 0, 0, 0, 0, 0, 0, 0))
    print(max_geodes, 'geode{} obtainable'.format('s'*int(max_geodes!=1)))
    print('Took', process_time() - prev_time, 'sec')
    final_result += blueprint_id * max_geodes
# for item in sorted(most_geodes_obtainable.items(), key=lambda c: c[0]):
#     print(item)