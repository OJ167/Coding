import random
import string

from numpy import character
from words import words

def get_valid_word(words):
    word = random.choice(words)
    while "-" in word or " " in word:
        word = random.choice(words)
    
    return word.upper()

def hangman():
    word = get_valid_word(words)
    word_letters = set(word) #letters in the word
    alphabet = set(string.ascii_uppercase) 
    used_letters = set() # what the user has guessed

    lives = 7

    #getting user input
    while len(word_letters) > 0 and lives > 0 :
        # words used
        print("You have", lives, "lives left and you have used these letters: ", " ".join(used_letters))

        # what current word is (e.g w o _ d)
        word_list = [letter if letter in used_letters else "_ " for letter in word]
        print("Current word: ", " ".join(word_list))

        user_letter = input("what is your letter? ").upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                lives = lives - 1
        
        elif user_letter in used_letters:
            print("you've alreaddy guessed that!")

        else:
            print("invalid character" )

    if lives == 0:
        print("you died and the word was", word)
    else:
        print("You guessed the word, ", word)
        
hangman()