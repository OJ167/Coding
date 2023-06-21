#          01234567890123456789012345
#          54321098765432109876543210  
letters = "abcdefghijklmnopqrstuvwxyz"

backwards = letters[::-1]
print(backwards)

#qpo
qpo = letters[16:13:-1]
print(qpo)

#edcba
edcba = letters[4::-1]
print(edcba)

#last 8 characters in reverse
last_8 =  letters[:-9:-1] #negative step means the start defaults to the last character
print(last_8)

#return the last n characters in a sequence
print(letters[-4:])
print(letters[-1:])
print(letters[:1]) #This will work with empty sequence
print(letters[0]) #this will not work with empty sequence