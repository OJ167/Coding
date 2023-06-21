#
#         012345678901234  
parrot = "Norwegian Blue"

print(parrot[0:6:2]) #start:end:step size
print(parrot[0:6:3])

number = "1,654;898:756 215,657;807"
separators = number[1::4]
print(separators)

values = "".join(char if char not in separators else " " for char in number).split()
print([int(val) for val in values])