import numpy as np
import os
import sys
import mat73
from scipy.interpolate import make_interp_spline, BSpline
from scipy import io
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import pandas as pd
import matplotlib.colors as colors
import matplotlib.cm
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
from scipy.interpolate import RectBivariateSpline
import h5py
# from colorspacious import cspace_converter

#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)


####Import Ollie Tools MAC
# dirPath = "/Users/olliejackson/Coding"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)

##### Set plot style #####
plt.style.use(["science", "vibrant", "no-latex"])
cmap = plt.get_cmap("bwr")



Rotations = ['RPM0', 'RPM1', 'RPM2', 'RPM3', 'RPM6', 'RPM9', 'RPM12']
Injection = ['U50', 'U100']
Stroke = ['L50', 'L100']
I = 'U100'
S = 'L50'

h5file = h5py.File('E:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)][str(S)][str(Rotations[0])]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
time = oj.frames_to_seconds(u, u, 90)
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])

vort, vortGauss = oj.calculate_vorticity(u, v)

# contour_value = [0.1]

# f1, ax1  = plt.subplots()
# ax1.contour(vortGauss[300,:,:], levels=[contour_value], cmap = "bwr")

contour_value = [-0.5, 0.5]

contours = plt.contour(z_nd, r_nd, vortGauss[300,:,:], contour_value, colors='black')
plt.clabel(contours, inline=True, fontsize=8)

plt.contourf(u[300,:,:], extent=[z_nd[0], z_nd[-1], r_nd[0], r_nd[-1]], cmap='bwr')
plt.colorbar()

plt.show()

contour_points = contours.get_paths()[0].vertices
contour_points = sorted(contour_points, key=lambda point: point[0])
