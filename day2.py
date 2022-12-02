with open('./input2.txt') as f:
    data = f.read()
matches = data.split('\n')[:-1]

draws = {'A X', 'B Y', 'C Z'}
wins = {'A Y', 'B Z', 'C X'}
losses = {'A Z', 'B X', 'C Y'}
score = {'X': 1, 'Y': 2, 'Z': 3}

# part 1
total = 0
for round in matches:
    total += 6*int(round in wins) 
    total += 3*int(round in draws) 
    total += score[round[-1]]
print(total)

# part 2
condition_score = {'X': 0, 'Y': 3, 'Z': 6}
correspondence = {'X': losses, 'Y': draws, 'Z': wins}
total = 0
for round in matches:
    result = [item for item in correspondence[round[-1]] if round[0]==item[0]][0]
    total += condition_score[round[-1]]
    total += score[result[-1]]
print(total)
