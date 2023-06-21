####
## Asking user which process they want to check
####

task = input("Check if Odd or Even? [y/n]")

####
## Check if a number is odd or even
####

if task == "y":

    num = round(float(input("Odd or even:")))

    if num%4 ==0: 
        print(num, "is even and divisible by 4!")
    elif num%2 ==0:
            print(num, "is even")
    else:
        print(num, "is odd")


####
## Now asking for 2 inputs and checking for if they are factors of each-other
####

else:
    
    Numerator = float((input("What is your first number?:")))
    Denominator =  float((input("What is your second number?:")))

    if Numerator%Denominator ==0:
        print(int(Denominator), "is a factor of", int(Numerator))

    else:
        print(int(Denominator), "is not a factor of", int(Numerator))