#
#         012345678901234  
# parrot = "Norwegian Blue"

# print(parrot[0:6:2]) #start:end:step size
# print(parrot[0:6:3])

number = input("Please enter a series of numbers using any separators you like: ")
separators = ""
for char in number:
    if not char.isnumeric():
        separators = separators + char

#print(separators)

values = "".join(char if char not in separators else " " for char in number).split()
print(sum([int(val) for val in values]))