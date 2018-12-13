import re
import random
import numpy as np

"""Where we are, currently get a correct list of lists of the string in a funny order
Need to reverse the final list and all the sublists to have a correct half a matrix and account for dodgy characters"""

def find_best_start(tour_matrix):
    for i in range(len(tour_matrix - 1)):
        return

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


def max_distance(matrix):
    total = 0
    for item in matrix:
        for num in item:
            total += num
    return total

def calculate_distance(list, matrix):
    total_distance = 0
    for i in range(len(list)-1):
        x, y = correct_orientation(list[i], list[i+1])
        total_distance += matrix[x-1][y-1]
    x, y = correct_orientation(list[0], list[-1])
    total_distance = total_distance + matrix[x-1][y-1]
    #print("Total distance of this tour is: " + str(total_distance))
    return total_distance

def correct_orientation(x, y):
    if y > x:
        return x, y
    return y, x

def random_neighbouring_solution(next_tour):
    length = range(len(next_tour))
    a, b = random.sample(length, 2)
    next_tour[a], next_tour[b] = next_tour[b], next_tour[a]
    print(next_tour)
    return next_tour

def random_close_neighbouring_solution(next_tour):
    length = len(next_tour)
    a = random.randint(0, length-1)
    if a == 0:
        next_tour[a], next_tour[a + 1] = next_tour[a + 1], next_tour[a]
        return next_tour
    next_tour[a], next_tour[a-1] = next_tour[a-1], next_tour[a]
    return next_tour

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

def probability_acceptance(curr_distance, new_distance, temperature):
    if new_distance < curr_distance:
        return 1
    if curr_distance == new_distance:
        return 0
    return np.exp((curr_distance - new_distance)/temperature)


def annealing_algorithm(tour_matrix):
    size_tour = len(tour_matrix)+1
    #temperature = max_distance(tour_matrix)
    temperature = 25000000
    #print(temperature)
    minimum_temperature = 0.000001
    alpha = 0.99
    curr_tour = [x for x in range(1, size_tour + 1)]
    #curr_tour = [482, 158, 418, 328, 89, 65, 195, 500, 446, 403, 19, 128, 485, 230, 343, 349, 52, 325, 426, 54, 380, 101, 298, 295, 182, 455, 166, 68, 183, 341, 181, 74, 165, 525, 206, 507, 70, 307, 395, 517, 457, 323, 215, 154, 391, 167, 227, 390, 55, 102, 529, 3, 160, 56, 235, 510, 434, 474, 109, 358, 200, 501, 98, 186, 2, 201, 340, 90, 187, 377, 360, 350, 283, 117, 226, 516, 459, 242, 14, 34, 453, 289, 386, 78, 30, 75, 292, 174, 290, 296, 79, 458, 526, 445, 64, 462, 202, 361, 83, 291, 452, 237, 153, 461, 521, 151, 511, 530, 497, 134, 204, 234, 172, 392, 251, 400, 494, 81, 6, 269, 222, 491, 236, 394, 17, 468, 488, 4, 281, 393, 253, 362, 21, 378, 423, 232, 244, 45, 96, 326, 171, 116, 301, 407, 184, 268, 157, 430, 398, 28, 20, 207, 304, 293, 238, 412, 439, 254, 126, 190, 351, 273, 66, 203, 80, 441, 280, 127, 188, 246, 518, 262, 48, 7, 245, 431, 50, 192, 58, 173, 51, 384, 308, 406, 438, 259, 233, 339, 338, 208, 129, 319, 85, 143, 205, 335, 495, 224, 493, 91, 10, 194, 388, 365, 199, 112, 383, 37, 177, 137, 95, 38, 447, 216, 524, 240, 411, 99, 317, 329, 282, 498, 27, 138, 300, 496, 432, 106, 321, 135, 193, 422, 77, 265, 12, 463, 414, 132, 464, 161, 487, 140, 303, 67, 330, 191, 346, 24, 342, 363, 123, 451, 416, 231, 469, 410, 9, 299, 271, 214, 144, 389, 49, 255, 347, 481, 42, 8, 535, 62, 258, 270, 133, 105, 436, 39, 302, 368, 179, 147, 197, 475, 229, 490, 100, 225, 263, 514, 344, 176, 211, 124, 119, 163, 120, 471, 59, 287, 221, 217, 315, 185, 272, 515, 405, 427, 348, 421, 267, 396, 93, 125, 372, 370, 131, 437, 470, 509, 103, 13, 531, 417, 401, 57, 169, 519, 369, 306, 285, 178, 419, 382, 337, 94, 257, 136, 512, 371, 228, 385, 210, 476, 220, 156, 114, 357, 41, 528, 248, 523, 15, 484, 483, 198, 86, 443, 115, 478, 278, 148, 359, 11, 130, 122, 223, 104, 26, 367, 256, 479, 415, 492, 324, 513, 22, 534, 18, 61, 532, 180, 212, 520, 82, 155, 31, 508, 429, 284, 309, 334, 274, 97, 276, 63, 5, 249, 460, 366, 32, 404, 29, 450, 413, 175, 73, 69, 36, 465, 364, 376, 264, 503, 527, 275, 373, 84, 35, 454, 219, 16, 25, 472, 87, 399, 522, 312, 168, 333, 420, 318, 53, 72, 424, 239, 47, 433, 164, 218, 473, 374, 402, 408, 150, 444, 435, 40, 277, 327, 261, 113, 209, 260, 159, 448, 313, 139, 43, 46, 466, 489, 506, 355, 320, 322, 146, 247, 142, 480, 440, 288, 145, 243, 121, 356, 118, 305, 196, 533, 502, 60, 110, 88, 486, 92, 189, 352, 170, 250, 152, 297, 294, 279, 336, 449, 314, 505, 332, 456, 23, 76, 149, 108, 409, 44, 467, 286, 477, 111, 428, 107, 354, 381, 387, 213, 141, 162, 375, 252, 353, 442, 311, 241, 266, 345, 504, 397, 499, 379, 316, 331, 71, 1, 310, 425, 33]

    curr_distance = calculate_distance(curr_tour, tour_matrix)
    #print("FIRST DISTANCE = " + str(curr_distance))
    while temperature > minimum_temperature:
        count = 1
        while count < 100:

            new_tour = reversed_neighbouring_solution(curr_tour[:])

            new_distance = calculate_distance(new_tour, tour_matrix)
            pa = probability_acceptance(curr_distance, new_distance, temperature)

            random_num = random.uniform(0, 1)
            if pa > random_num:
                curr_tour = new_tour
                curr_distance = new_distance

            count += 1
        temperature = temperature*alpha
        #temperature = temperature - 0.2
        #print(temperature)
        #temperature = temperature*(1/(1 + (temperature*0.5)))
        #print(temperature)
    return curr_tour, curr_distance


def correct_output(tour, distance):
    print("Best Tour = " + str(tour))
    print("Shortest Distance = " + str(distance))
    """final_file = open("tourAISearchtestcase", "w+")

    final_file.write("NAME = AISearchtestcase,\n")

    final_file.write("TOURSIZE = " + str(len(tour) - 1) + '\n')

    final_file.write("LENGTH = " + str(distance) + '\n')

    final_file.write(str(tour))
    final_file.close()"""


def begin(num_tour):
    print("Simulated Annealing Algorithm")
    f = open("NEWAISearchfile" + num_tour + ".txt", "r")
    file_string = f.read()
    file_string = file_string.replace('\n', '')
    file_list = file_string.split(',')
    file_list[0] = file_list[0].replace('NAME = ', '')
    file_list[1] = file_list[1].replace('SIZE = ', '')
    num_of_cities = int(file_list[1])
    distances = file_list[2:]
    tour_matrix = create_search_matrix(num_of_cities, distances)
    f.close()
    total = 0
    best_ever_distance = np.inf
    best_ever_tour = []
    for i in range(10):
        print("------------------NEW---------------------")
        best_tour, best_distance = annealing_algorithm(tour_matrix)
        correct_output(best_tour, best_distance)
        if(best_distance < best_ever_distance):
            best_ever_distance = best_distance
            best_ever_tour = best_tour
        total = total+best_distance
    print("------------FINISH-----------")
    return best_ever_distance, best_ever_tour, total


tour = input("Which tour?")
tour, distance, total = begin(tour)
print("Best Distance = " + str(distance))
print("Best Tour = " + str(tour))
print(total/10)