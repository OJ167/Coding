import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.optimize import curve_fit #from internet
from scipy.optimize import least_squares #from internet

from scipy.interpolate import make_interp_spline, BSpline#from sam
#np.polyfit
from scipy.signal import savgol_filter #my old fave


plt.style.use(['notebook', 'grid'])


N = 360 # Number of samples
T = 1 # Sample Spacing
x = np.linspace(0.0, N*T, N, endpoint=False)
x = np.arange(0, 1, 1/360)
y = np.sin(2*2*np.pi*x)+random.uniform(0.9, 1.10)

for i in range(len(y)):
    y[i] = y[i]+random.uniform(-0.2, 0.2)

# plt.scatter(x, y)
# plt.show()

savgol = savgol_filter(y, 50, 3)
polyfit = np.poly1d(np.polyfit(x, y, 11))(x)


f2, ax2 = plt.subplots()
ax2.scatter(x, y)
ax2.plot(x, savgol)
ax2.plot(x, polyfit)
# plt.show()


quad = x**2

for i in range(len(quad)):
    quad[i] = quad[i]+random.uniform(-0.1, 0.1)

quad_savgol = savgol_filter(quad, 50, 3)
quad_polyfit = np.poly1d(np.polyfit(x, quad, 2))(x)


f3, ax3 = plt.subplots()
ax3.scatter(x, quad)
ax3.plot(x, quad_savgol)
ax3.plot(x, quad_polyfit)
# plt.show()


cube = 10*(x-0.5)**3

for i in range(len(quad)):
    cube[i] = cube[i]+random.uniform(-0.1, 0.1)

cube_savgol = savgol_filter(cube, 50, 3)
cube_polyfit = np.poly1d(np.polyfit(x, cube, 3))(x)

plt.style.use(['science', 'no-latex', 'grid'])

f4, ax4 = plt.subplots()
ax4.scatter(x, cube)
ax4.plot(x, cube_savgol)
ax4.plot(x, cube_polyfit)
plt.savefig('C:/Users/u2088308/Videos/3D0_100_100/plot1.png', dpi = 200)
plt.show()