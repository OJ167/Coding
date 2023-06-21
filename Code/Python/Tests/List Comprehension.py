####
## Code to filter a list and only retun the even elements.
####

a = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
b = []


for elements in a: 
    if elements %2 ==0:
        b.append(elements)

## attempt to do it in one line from the internet.
c = [elements for elements in a if elements %2 ==0]

print("b is equal to:", b)
print("c is equal to:", c)

## attempt to use a random number generator to make a random list

import random

rand_list = []
list_length = random.randint(0,15)

d = [elements for elements in rand_list if elements %2 ==0]
print(d)

import random
f = random.sample(range(1000000),random.randint(0,150))
g = [elements for elements in f if elements %2 !=0]
print(f)
print(g)