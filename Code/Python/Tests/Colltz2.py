import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import scipy.fft as sp

# input_number = 27
input_range = 10000000
steps = 0
answer_list = []


def Collatz_maths(input_number, steps):
    current_number = input_number
    # print(current_number)
    while current_number != 1:
        # print(steps)
        steps = steps + 1
        # print("Steps: " + str(steps))
        if current_number %2 == 0:
            # print(current_number)
            current_number = int(current_number/2)
            # print("Current number: " + str(current_number))
        
        else:
            # print(current_number)
            current_number = int(3 * current_number + 1)
            # print("Current number: " + str(current_number))
    return steps


for i in range(1, input_range + 1):
    print("input number: " + str(i))
    input_number = i
    stop_time = Collatz_maths(input_number, steps)

    data = (input_number, stop_time)
    # print(data)

    answer_list.append(data)
# print(answer_list)

start_number = [x[0] for x in answer_list]
step_number = [x[1] for x in answer_list]

# print(start_number)
# print(step_number)

longest_chain = np.where(max(step_number)) 
print(longest_chain)

f1, ax1 = plt.subplots()
ax1.scatter(start_number[:], step_number[:])


f2, ax2 = plt.subplots()
ax2.plot(start_number[:], np.gradient(step_number[:]))


fft = sp.fft(np.gradient(step_number[:]))

f3, ax3 = plt.subplots()
ax3.plot(start_number[:], fft)
plt.show()