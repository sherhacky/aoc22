import itertools
import collections
from time import process_time

with open('./input18.txt') as f:
    data = f.read()

cube_strings = data.split('\n')[:-1]
cubes = set([eval(cube_string) for cube_string in cube_strings])

# part 1
def faces(cube):
    x,y,z = cube
    result = []
    for shift in [0, 1]:
        for coord in [0, 1, 2]:
            ranges = [[0,1] if axis != coord else [shift] for axis in range(3)]
            result.append(frozenset((x+i, y+j, z+k) for i in ranges[0] for j in ranges[1] for k in ranges[2]))
    return(frozenset(result))

def exterior_surface_area(cubes):
    all_faces = [face for cube in cubes for face in faces(cube)]
    face_count = collections.Counter(all_faces)
    return len([face for face, count in face_count.items() if count == 1])

print(exterior_surface_area(cubes))

# part 2
def neighbors(location):
    shifts = [0,0,1], [0,0,-1], [0,1,0], [0,-1,0], [1,0,0], [-1,0,0]
    return {tuple(location[i] + shift[i] for i in range(3)) for shift in shifts}

def connected_component(cube_set, location, extremes=[-float('inf'), float('inf')]):
    if location in cube_set:
        return None
    component = set()
    queue = {location}
    while queue:
        cube = queue.pop()
        component.add(cube)
        for next_cube in neighbors(cube):
            if next_cube not in component | cube_set \
              and all([extremes[0] < next_cube[i] < extremes[1] for i in range(3)]):
                queue.add(next_cube)
    return component

extremes = [func(cube[i] for i in range(3) for cube in cubes) for func in (min, max)]
exterior = connected_component(set(cubes), (extremes[0]-1,)*3, [extremes[0]-2, extremes[1]+2])
interior = set()
interior_surface_area = 0
for i,j,k in itertools.product(range(extremes[0], extremes[1]+1), repeat=3):
    if (i,j,k) not in cubes | exterior | interior:
        interior_component = connected_component(cubes, (i,j,k))
        interior_surface_area += exterior_surface_area(interior_component)
        interior |= interior_component
    
print(exterior_surface_area(cubes) - interior_surface_area)
print('Took {} seconds'.format(process_time()))
