import time

with open('./input15.txt') as f:
    data = f.read()

rows = data.split('\n')[:-1]

pairs = []
for line in rows:
    p = line.split(' ')
    [sensor, beacon] = [[int(p[2].split('=')[1][:-1]), int(p[3].split('=')[1][:-1])],
                        [int(p[-2].split('=')[1][:-1]), int(p[-1].split('=')[1])]]
    pairs.append([sensor, beacon])

# part 1
def omitted_positions(pairs, y):
    omitted = set()
    not_omitted = set()
    for [sensor, beacon] in pairs:
        distance = sum([abs(sensor[i] - beacon[i]) for i in [0,1]])
        [a, b] = sensor
        if abs(y-b) <= distance:
            for i in range(distance-abs(y-b)+1):
                omitted.add(a+i)
                omitted.add(a-i)
        if beacon[1] == y:
            not_omitted.add(beacon[0])
    omitted -= not_omitted
    return omitted

print(len(omitted_positions(pairs, 2000000)))

# part 2
def disjointify(intervals):
    left_endpoints = {x for (x,y) in intervals if all([not(a<x<b) for (a,b) in intervals])}
    right_endpoints = {y for (x,y) in intervals if all([not(a<y<b) for (a,b) in intervals])}
    result = []
    for x in sorted(left_endpoints):
        y = min(u for u in right_endpoints if u > x)
        result.append((x,y))
    return result

def find_first_point_not_in_intervals(max_value):
    for y in range(max_value):
        endpoints = []
        for [sensor, beacon] in pairs:
            distance = sum([abs(sensor[i] - beacon[i]) for i in [0,1]])
            [a, b] = sensor
            if abs(y-b) <= distance:
                i = distance-abs(y-b)
                endpoints.append((a-i, a+i))
        endpoints = disjointify(endpoints)
        for i in range(len(endpoints)-1):
            if endpoints[i][1] < endpoints[i+1][0]-1:
                x = endpoints[i][1] + 1
                return x,y

max_value = 4000000
x,y = find_first_point_not_in_intervals(max_value)
print(4000000*x + y)
print('running the thing took', time.process_time(), 'seconds')
