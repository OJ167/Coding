def Print_return(name):
    """return the message with a greeting"""
    print("Hello! " +  name  + " How are you?")

username = input("What is your name?")
Print_return(username)

def add_numbers(x,y):
    """
    Add two numbers together
    """
    sum = x + y
    return sum

num1 = int(input("number 1:"))
num2 = int(input("number 2:"))

print("Sum of two numbers is ", add_numbers(num1, num2))
print(type(num1))
print(type(num2))