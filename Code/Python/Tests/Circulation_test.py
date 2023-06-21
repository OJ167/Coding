import numpy as np
import os
import sys
import mat73
from scipy.interpolate import make_interp_spline, BSpline
from scipy import io
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
import pandas as pd
import matplotlib.colors as colors
import matplotlib.cm
# from colorspacious import cspace_converter

#####Import Ollie Tools
dirPath = "C:/Coding/Code"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)

x, y = np.meshgrid(np.arange(-2, 2, 0.25), np.arange(-2, 2, 0.25))

####Divirging flow - F(x, y) = xi + yj

u = x/np.sqrt(x**2 + y**2)
v = y/np.sqrt(x**2 + y**2)


f1, ax1 = plt.subplots()
ax1.quiver(x, y, u, v, pivot = "middle")
plt.show()


####Swirling Flow - F(x, y) = -yj + xi

u = -y/np.sqrt(x**2 + y**2)
v = x/np.sqrt(x**2 + y**2)

f2, ax2 = plt.subplots()
ax2.quiver(x, y, u, v, pivot = "middle")
plt.show()


# Define the contour.
x_contour = np.linspace(-1, 1, 100)
y_contour = 0

# Calculate the circulation.
circulation = 0
for i in range(len(x_contour) - 1):
  # Calculate the velocity vector at the current point.
  vx_current = u[i]
  vy_current = v[i]

  # Calculate the contour vector at the current point.
  dx = x_contour[i + 1] - x_contour[i]
  dy = y_contour[i + 1] - y_contour[i]

  # Dot the velocity vector and the contour vector.
  dot_product = vx_current * dx + vy_current * dy

  # Add the dot product to the circulation.
  circulation += dot_product

print(circulation)