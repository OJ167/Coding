#import random
#
#highest = 10
#answer = random.randint(1,highest)
#print(answer) # TODO: Remove after testing
#
#print("Please guess a number between 1 and {}: ".format(highest))
#guess = int(input())
#
#if guess == answer:
#    print("You got it first time")
#else:
#    if guess < answer:
#        print("Please guess higher")
#    else: # guess must be greater than answer
#        print("Please guess lower")
#    guess = int(input())
#    if guess == answer:
#        print("Well done, you have guessed it")
#    else:
#        print("Sorry, you have not guessed correctly")


import random

highest = 10
answer = random.randint(1,highest)

print("Please guess a number between 1 and {}: ".format(highest))
guess = 0

while guess != answer:
    guess = int(input())

    if guess == 0:
        break

    if guess == answer:
        print("Well done, you have guessed it")
        break
    else:
        if guess < answer: # guess must be greater than answer
            print("Please guess higher")
                
        else: 
            print("Please guess lower")
