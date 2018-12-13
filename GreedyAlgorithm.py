import re
import numpy as np
"""Where we are, currently get a correct list of lists of the string in a funny order
Need to reverse the final list and all the sublists to have a correct half a matrix and account for dodgy characters"""

def create_search_matrix(size, list):
    print("here")
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

    print(distance_list)

    return distance_list

def begin():
    f = open("AISearchtestcase.txt", "r")
    file_string = f.read()
    file_string = file_string.replace('\n', '')
    file_list = file_string.split(',')
    file_list[0] = file_list[0].replace('NAME = ', '')
    file_list[1] = file_list[1].replace('SIZE = ', '')

    name_of_case = file_list[0]
    num_of_cities = int(file_list[1])

    distances = file_list[2:]
    create_search_matrix(num_of_cities, distances)
    print(create_search_matrix(num_of_cities, distances))
    f.close()
    return

begin()