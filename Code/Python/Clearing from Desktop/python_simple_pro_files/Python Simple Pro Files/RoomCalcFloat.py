#Calculates area

print("Room dimensions calculator:")

#Input the width and length
width = float(input("What is the room width in metres? "))
length = float(input("What is the room length in metres? "))

#Output the area
print("The room is", width, "by", length, "giving a total area of", round(width*length,1), "metres square.")
