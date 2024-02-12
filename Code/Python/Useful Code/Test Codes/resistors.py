import numpy as np
import matplotlib.pyplot as plt

# Question 2
Res = np.array([[3, 2, 3, 10],[2, -2, 5, 8],[3, 3, 4, 9],[3, 4, -3, -7]])
Val = np.array([4, 1, 3, 2])

a = np.linalg.solve(Res, Val)
print(a)



# Question 3
z = np.linspace(0, 10, 1000)
t = np.linspace(0, 4*np.pi, 1000)
zv, tv = np.meshgrid(z, t)

Ex = np.cos(zv-tv)
Ey = 2*np.cos(zv-tv+np.pi/2)
Ez = 0*zv 

# plt.plot(t, Ex[0,:])
# plt.plot(z, Ex[:,0])
# plt.show()


E = np.array([Ex, Ey, Ez])
E = np.swapaxes(E, 0, -1)

B = np.cross(np.array([0,0,1]), E)
B = np.swapaxes(B, 0, -1)

Bx, By, Bz = B
# plt.plot(t,Ey[0])
# plt.plot(t,Bx[0])
# plt.show()


#Question 1

x = np.linspace(-2, 2, 1000)
y = np.linspace(-2, 2, 1000)
Xv, Yv = np.meshgrid(x, y)

f = np.exp(-(Xv**2 + Yv**2)) * np.sin(Xv)



V = np.abs(f.ravel()).sum() * np.diff(x)[0] * np.diff(y)[0]
print(V)

w = Xv**2 + Yv**2 > 0.5**2
A = np.abs(f[w]).sum() * np.diff(x)[0] * np.diff(y)[0]
print(A)
# plt.contourf(Xv, Yv, f, levels = 30)

#Part 1 Questions
#Question 1
x = np.linspace(0, 10, 10000)
y = np.exp(-x/10)*np.sin(x)


xmean = np.mean(y[(x>=4)*(x<=7)])
std = np.std(y[(x>=4)*(x<=7)])
print(xmean)
print(std)

perc = np.percentile(y[(x>=4)*(x<=7)], 80)
print(perc)

dydx = np.gradient(y, x)

roots = x[1:][dydx[1:] * dydx[:-1] < 0]

print(roots)
# plt.plot(x, y)
# plt.plot(x, dydx)

#question 2
nums = np.arange(0, 10001, 1)
suma = sum(nums[(nums%4 != 0) * (nums%7 != 0)])
print(suma)

#question 3
theta = np.linspace(0, 2*np.pi, 1000)
r = 1 + 3/4 * np.sin(3*theta)
x = r * np.cos(theta)
y = r * np.sin(theta)

A = 1/2 * sum(r**2) * (theta[1] - theta[0])
print(A)
 
A = 1/2 * sum(r**2) * np.diff(theta)[0] 
print(A)

L = sum(np.sqrt(r**2 + np.gradient(r, theta)**2) * np.diff(theta)[0])
print(L)

plt.plot(x,y)
plt.show()

#question 4
