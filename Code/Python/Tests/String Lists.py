####
## Ask user to input a string and see if it is a palindrome
####

a = input("input your string:")

# Reversing the list the user inputs
b = a[::-1]

if a == b:
    print("your string is a palindrome!")
else:
    print("your string is not a palindrome!")