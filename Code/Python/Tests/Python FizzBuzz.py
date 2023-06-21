# FizzBuzz test code
# Numbers divisivle by 3 become "Fizz"
# Numbers divisivle by 5 become "Buzz"
# Numbers divisivle by both become "FizzBuzz"

x = "fizz"
y = "buzz"
z = "FIZZBUZZ!!!"
temp = 0

while temp <= 99:
    temp +=1
    if temp%3 == 0 and temp%5 == 0:
        print(z)

    elif temp%3 == 0:
        print(x)
        
    elif temp%5 == 0:
        print(y)

    else:
        print(temp)
