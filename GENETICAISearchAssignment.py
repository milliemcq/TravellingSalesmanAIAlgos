import re
import random
import math

"""
Seems to return correct tours

TODO:
- Figure out how to have a global variable for best_distance and best_tour
- Test again 
"""

#Global variables needed throughout code
best_distance = math.inf
best_tour = []

#Creates the distance matrix of distances between cities
def create_search_matrix(size, list):
    distance_list = []
    curr_location = 0
    for i in range(size, 1, -1):
        curr_list = []
        diff = size - i + 1
        for k in range(diff):
            curr_list.append(0)
        for j in range(i-1):
            list[curr_location] = re.sub("[^0-9]", "", list[curr_location])
            curr_list.append(int(list[curr_location]))
            curr_location +=1

        distance_list.append(curr_list)

    #print(distance_list)

    return distance_list


#calculates the distance of a given tour
def calculate_distance(list, matrix):
    #print("Calculate distance list: " + str(list))
    #print(list)
    total_distance = 0
    for i in range(len(list)-1):
        x, y = correct_orientation(list[i], list[i+1])
        total_distance += matrix[x-1][y-1]
    x, y = correct_orientation(list[0], list[-1])
    total_distance = total_distance + matrix[x-1][y-1]
    #print("Total distance of this tour is: " + str(total_distance))
    return total_distance


#ensures we are only ever searching the top right of our matrix
def correct_orientation(x, y):
    if y > x:
        return x, y
    return y, x


#creates a random tour with two characters swapped from given tour
def mutate(curr_tour, mutation_rate):
    length = range(len(curr_tour))
    if(random.uniform(0,1) < mutation_rate):
        a, b = random.sample(length, 2)
        curr_tour[a], curr_tour[b] = curr_tour[b], curr_tour[a]
    return curr_tour


def mutate_reverse(curr_tour, mutation_rate):
    length = range(len(curr_tour))
    if (random.uniform(0, 1) < mutation_rate):
        return reversed_neighbouring_solution(curr_tour)
    return curr_tour


def partial_reverse(lst, start, end):
    return lst[:start] + lst[start:end+1][::-1] + lst[end+1:]

def reversed_neighbouring_solution(next_tour):
    length = range(len(next_tour))
    a, b = random.sample(length, 2)

    if a < b:
        next_tour = partial_reverse(next_tour, a, b)

        return next_tour
    elif b < a:
        next_tour = partial_reverse(next_tour, b, a)
        return next_tour
    return next_tour

#creates a population from a given initial tour, returning a list of shuffled tours
def create_population(init_tour, num):
    population = []
    for i in range(num):
        population.append(random.sample(init_tour, len(init_tour)))
    return population


#creates a fitness value which can be used like a probability
def normalise_fitness(fitness_values):
    norm = [float(i) / sum(fitness_values) for i in fitness_values]
    return norm


#Creates a new tour by breeding two previous tours
def cross_over(tourA, tourB):
    new_order = []
    begin = random.randint(0, len(tourA))
    end = random.randint(begin+1, len(tourA) + 1)

    new_order.extend(tourA[begin:end])

    num_left = len(tourA) - len(new_order)

    for item in tourB:
        if item not in new_order:
            new_order.append(item)

    return new_order


def pmx_crossover(tourA, tourB):
    n = len(tourA)
    new_order = [0] * n

    begin = random.randint(0, n)
    end = random.randint(begin + 1, n + 1)

    new_order[begin:end] = tourA[begin:end]

    for item in tourB[begin:end]:
        repeat = True
        while repeat:
            if item not in new_order:
                index = tourB.index(item)
                value = tourA[index]
                index = tourB.index(value)
                if index in range(begin, end):
                    item = value
                    continue
                else:
                    new_order[index] = item
                    repeat = False
            else:
                repeat = False

    # print("nid: " + str(new_order))

    while 0 in new_order:

        for i in range(n):
            if new_order[i] == 0:
                for value in tourB:
                    if value not in new_order:
                        new_order[i] = value
                        value = 1

    return new_order


#creates the next population generation by selectively choosing the best tours
def next_generation(population, fitness_values, rate):
    new_population = []
    for i in range(len(population)):
        selected_tour_A = pick_one_random(population, fitness_values)
        selected_tour_B = pick_one_random(population, fitness_values)
        new_tour_descendant = cross_over(selected_tour_A, selected_tour_B)
        selected_tour = mutate(new_tour_descendant, rate)
        new_population.append(selected_tour)
    return new_population


#picks any random tour from our population, the better the tour, the more likely it will be picked
def pick_one(population, fitness_values):
    index = 0
    prob = random.uniform(0,1)
    while prob > 0:
        prob = prob - fitness_values[index]
        #print("Prob = " + str(prob))
        index += 1
    index -= 1
    return population[index]

def pick_one_random(population, fitness_values):
    return random.choice(population)


#creates a list of fitness for our population matrix (fitness = distance) also helps us find the best length so far
def create_fitness_list(tour_matrix, population):
    global best_distance
    global best_tour
    #print(best_distance)
    fitness = []
    for i in range(len(population) - 1):
        distance = calculate_distance(population[i], tour_matrix)

        if distance < best_distance:
            best_distance = distance
            best_tour = population[i]
        fitness.append(1/(distance+1))
    return fitness


#genetic algorithm overview, can choose the number of times you want to mutate here
def genetic_algorithm(tour_matrix, rate, population_size):
    #initialise the size of our tour and the initial tour route
    size_tour = len(tour_matrix) + 1
    init_tour = [x for x in range(1, size_tour + 1)]

    #create our population and calculate the fitness of this population
    population = create_population(init_tour, 5)
    fitness_list = create_fitness_list(tour_matrix, population)
    normalised_fitness = normalise_fitness(fitness_list)
    for i in range(population_size):
        population = next_generation(population, normalised_fitness, rate)
        fitness_list = create_fitness_list(tour_matrix, population)
        normalised_fitness = normalise_fitness(fitness_list)

    return best_distance, best_tour



def correct_output(tour, distance):
    print("Best Tour = " + str(tour))
    print("Shortest Distance = " + str(distance))
    """final_file = open("RESULTAISearchtestcase", "w+")
    final_file.write("NAME = AISearchtestcase,")
    final_file.write("TOURSIZE = " + str(len(tour) - 1))
    final_file.write("LENGTH = " + str(distance))
    final_file.write(str(tour))
    final_file.close()"""


def begin(num_tour, rate, population_size):
    #Reads and cleans the initial file
    #print("This is the genetic algorithm")
    f = open("NEWAISearchfile" + num_tour + ".txt", "r")
    file_string = f.read()
    file_string = file_string.replace('\n', '')
    file_list = file_string.split(',')
    file_list[0] = file_list[0].replace('NAME = ', '')
    file_list[1] = file_list[1].replace('SIZE = ', '')
    name_of_case = file_list[0]
    num_of_cities = int(file_list[1])
    distances = file_list[2:]
    tour_matrix = create_search_matrix(num_of_cities, distances)
    f.close()

    #begins our genetic algorithm and then converts it into the correct output
    #for i in range(100):
    print('-----------------------NEW TOUR-------------------------')
    best_distance, best_tour = genetic_algorithm(tour_matrix, rate, population_size)
    correct_output(best_tour, best_distance)


    return best_distance


#rate_values = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
#generation_values = [100, 200, 400, 800, 1600, 3200, 6400, 12800, 20000, 50000]
num_tour = input('Which tour?')


#print(item)
total = 0
for i in range(10):
    current = 0
    current = begin(num_tour, 0.65, 30000)
    total = total + current
    best_tour = []
    best_distance = math.inf
print('VALUE = ' + str(total / 10))


print('-------------------FINISH--------------------')

