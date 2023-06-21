import random

def play():
    user = input("'R' for rock, 'P' for paper, or 'S' for scissors: ").lower()
    computer = random.choice(["R", "P", "S"]).lower()

    if user == computer:
        return "tie"

    if is_win(user, computer):
        return "you won"

    return "you lost"

def is_win(player, opponent):
    # return true if player wins
    # r>s, s>p, p>r
    if (player == "r" and opponent == "s") or (player == "s" and opponent == "p") or (player == "p" and opponent == "r"):
        return True

print(play())