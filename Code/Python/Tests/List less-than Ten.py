####
## Find all the elements in the list that are smaller than a given value
####

x = float(input("What number would you like to check?:"))
a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b = []

for element in a:
    if element <= x:
        b.append(element)
    if element == x:
        print(element, "is present in the list") 
print(b)    


#### I cannot get it to work with the printed value below the list. 


c = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
x = float(input("What number would you like to check?:"))

for element in c if < x:
