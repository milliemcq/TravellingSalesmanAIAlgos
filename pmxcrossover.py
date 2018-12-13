import random

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
    new_order = [0]*n
    
    begin = random.randint(0, n)
    end = random.randint(begin+1, n + 1)
    
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


    #print("nid: " + str(new_order))

    while 0 in new_order:

        for i in range(n):
            if new_order[i] == 0:
                for value in tourB:
                    if value not in new_order:
                        new_order[i] = value
                        value = 1



    return new_order
    

a = [12, 4, 11, 2, 7, 8, 5, 1, 3, 9, 6, 10]
b = [12, 7, 1, 11, 10, 6, 5, 8, 2, 9, 3, 4]

for i in range(100):
	print(pmx_crossover(a, b))
print("--------------------------FINISH-----------------------")