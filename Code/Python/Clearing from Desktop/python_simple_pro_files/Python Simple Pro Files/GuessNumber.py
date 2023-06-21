#Guess the mystery number

#Assign mystery number
mysteryNumber = 10

print("Guess the mystery number game!")

#Ask for users guess
guessNumber = int(input("Guess the whole number?"))

#Check if guess is correct
if guessNumber == mysteryNumber:
    print("Your guess is correct!")
else:
    print("Your guess was wrong!")
print("Game over!")
