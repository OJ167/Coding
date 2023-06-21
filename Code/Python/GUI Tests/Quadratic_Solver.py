#quadratic equation solver to be used as GUI test
import cmath as maths
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

a = int(input("Coefficient of x^2: "))
b = int(input("Coefficient of x: "))
c = int(input("Constant: "))



print("Your equation is: {0}x^2 + {1}x + {2}".format(a,b,c)) 


#calculating the discriminant
dis = (b**2) - (4 * a * c)

#finding the two results
x = (-b + maths.sqrt(dis)) / (2 * a)
y = (-b - maths.sqrt(dis)) / (2 * a)

print("x is equal to {0}, {1}".format(x, y))

# fig = plt.figure()
# ax = plt.axes()

x = np.linspace(-1000, 1000, 1000)
plt.plot(x, ((a*x**5) + (b*x) + c))
plt.grid()
plt.show()