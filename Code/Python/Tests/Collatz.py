#### 3n + 1 problem
##

import numpy as np

# current_number = int(input("starting number: "))
group_size = 100
start_number = 5
current_number = start_number
steps = 1
stopping_time = 0
number_step = []
final_list = [] 


def collatz_calc(start_number, steps):

    stopping_time = 0

    current_number = start_number
    while current_number != 1:

        if current_number % 2 == 0:
            current_number = int(current_number/2)
            steps = steps + 1
            # print(current_number, steps)

        else:
            current_number = int(3*current_number + 1)
            steps = steps + 1
            # print(current_number, steps)

    print(stopping_time)
    stopping_time = steps
    print(stopping_time)
    number_step = [start_number, stopping_time]
    print(number_step)
    return number_step

for i in range(group_size):
    collatz_calc(start_number, steps)
    print(number_step)
    final_list.append(number_step)


print(number_step)


# print("loop has stopped in " + str(stopping_time) + "steps")
# print("loop has stopped in " + str(steps) + " steps")







# def func_even(current_number):
#     current_number = int(current_number/2)
#     return current_number
     
# def func_odd(current_number):
#     current_number = int(3*current_number + 1)
#     return current_number