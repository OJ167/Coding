#strings are a sequence data type
#         012345678901234
#negative 43210987654321              
parrot = "Norwegian Blue"

print(parrot)

print(parrot[5])

#Mini Challenge:
#       012345
text = "We Win"
for i in range (0, 6):
    print(text[i])

#Mini Challenge - reunderstood

print(parrot[3])
print(parrot[4])
print()
print(parrot[3])
print(parrot[6])
print(parrot[8])
print()

#mini challenge negative indexing
print(parrot[-11])
print(parrot[-1])
print()
print(parrot[-11])
print(parrot[-8])
print(parrot[-6])

#Mini Challenge - negative indexing 2

length = len(parrot)
print(parrot[3-length])
print(parrot[4-length])
print()
print(parrot[3-length])
print(parrot[6-length])
print(parrot[8-length])
print()