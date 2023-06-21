import random

from scipy import rand

def guess(x):
    randon_number = random.randint(1, x)
    guess = 0
    while guess != randon_number:
        guess = int(input(f"guess a number between 1 and {x}: "))
        print(guess)
        if guess < randon_number:
            print("sorry guess is too low")
        elif guess > randon_number:
            print("sorry guess is too high")

    print("Congratulations! you guessed the number correctly ")

def computer_guess(x):
    low = 1
    high = x
    feedback = ""
    while feedback != "c":
        if low != high:            
            guess = random.randint(low, high)
        else:
            guess = low
        feedback = input(f"is {guess} too high ('H'), too low ('L'), or correct ('C')?").lower()
        if feedback == "h":
            high = guess - 1

        elif feedback == "l":
            low = guess + 1
    print(f"the computer guessed {guess} correctly!")


computer_guess(10)