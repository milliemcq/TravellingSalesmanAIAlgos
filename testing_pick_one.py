import random

def pick_one(fitness_values):
    index = 0
    prob = random.uniform(0,1)
    while prob > 0:
        prob = prob - fitness_values[index]
        #print("Prob = " + str(prob))
        index += 1
    index -= 1
    return fitness_values[index]



def normalise_fitness(fitness_values):
    sum = 0
    for i in range(len(fitness_values)):
        sum += fitness_values[i]
        fitness_values[i] = fitness_values[i]/sum
    return fitness_values


def new_normalise(fitness_values):
    norm = [float(i) / sum(fitness_values) for i in fitness_values]
    return norm





test = [0.02439, 0.047619, 0.16, 0.1]
normalised = new_normalise(test)
for i in range(100):
    print(pick_one(normalised))
print(new_normalise(test))