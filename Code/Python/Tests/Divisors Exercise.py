####
## Ask for user input and return all the factors of the input number
####


i = int(input("What number would you like the factors of?:"))
a = []

for x in range(1,i):

    if i%x == 0:
        a.append(x)

print(a)