### Code to create an eulerian vortex ring model based on two Rankine vortex cores
import matplotlib.pyplot as plt
import numpy as np
import sys
from scipy.ndimage import gaussian_filter
import matplotlib.colors as colors
import matplotlib.cm

#####Import Ollie Tools
# dirPath = "C:/Coding"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)


####Import Ollie Tools MAC
# dirPath = "/Users/olliejackson/Coding"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)

##### Set plot style #####
plt.style.use(["science", "vibrant", "no-latex"])
matplotlib.rc('xtick', labelsize=8) 
matplotlib.rc('ytick', labelsize=8) 

x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(x, y)

Gamma = 1

x01, y01 = 0, 5
x02, y02 = 0, -5

u = -Gamma * (Y - y01) / ((X - x01)**2 + (Y - y01)**2) + Gamma * (Y - y02) / ((X - x02)**2 + (Y - y02)**2)
v = Gamma * (X - x01) / ((X - x01)**2 + (Y - y01)**2) - Gamma * (X - x02) / ((X - x02)**2 + (Y - y02)**2)

f1, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(5.5, 4))
ax1.plot(x, u[:,50], label = 'u', color = 'k')
plt.legend()
plt.show()