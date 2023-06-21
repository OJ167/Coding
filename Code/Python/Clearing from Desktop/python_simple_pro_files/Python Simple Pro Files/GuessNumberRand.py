#Guess random mystery number

import random

#Generate a random mystery number
mysteryNumber = random.randint(1,10)

#User guess number
guessNumber = int(input("Guess a whole number between 1 and 10?"))

#Check if guess is correct
if guessNumber == mysteryNumber:
    print("Your guess is correct!")
else:
    print("Your guess was wrong!")
    print("The mystery number was", mysteryNumber, "!")
print("The end!")
