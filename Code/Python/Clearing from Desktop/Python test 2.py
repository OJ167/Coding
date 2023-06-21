#Euler Problem 1 - sum of integers

total_sum = 0

for i in range(100):
    if (i%3 == 0 or i%4 == 0):
        total_sum = total_sum + i

print(total_sum)
