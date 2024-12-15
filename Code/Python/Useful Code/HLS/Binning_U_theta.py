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
import h5py
from matplotlib import animation
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




# h5file = h5py.File('E:/H5/3D0meandataHLS.h5', 'r')
h5file = h5py.File('E:/H5/3D0HLSFine.h5', 'r')

frame = 750
vels = h5file['3D0']['U100']['L100']['RPM0']
u = vels[:,:,:,0]
v = vels[:,:,:,1]
h5file.close()
u_gaussian, v_gaussian = gaussian_filter(u, sigma=6), gaussian_filter(v, sigma=6)
print(u.shape[0], u.shape[1], u.shape[2])

umean = np.mean(u, axis=0)
vmean = np.mean(v, axis=0)
V = np.sqrt(np.square(u_gaussian[:,:,:]) + np.square(v_gaussian[:,:,:]))

d = 0.025

x = 55
y = 35
x = np.linspace(0 , umean.shape[1], umean.shape[1])
y = np.linspace(0 , umean.shape[0], umean.shape[0])
X, Y = np.meshgrid(x, y) 

x_c, y_c, vort, vortSmooth = oj.find_vortex_center_Vorticity(u_gaussian[frame,:,:], v_gaussian[frame,:,:], guass = 6, range = 10)
r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(x_c, y_c, x, y, u_gaussian[frame,:,:], v_gaussian[frame,:,:])
r_arr, theta_arr, U_rBins, U_azBins = oj.binCylindrical(r, theta, U_r, U_az, thetaBins=5, rBins=5)




f1, (ax1, ax2, ax3) = plt.subplots(ncols=3)
ax1.plot(u_gaussian[frame, 76, :], label = "$du/dx$ at ")
# ax2.plot(U_r[ 35, :])
# cbar = ax2.contourf(u_gaussian[frame, :, :], cmap = 'seismic')
cbar = ax2.contourf(U_az[:, :], cmap = 'seismic')
f1.colorbar(cbar, ax=ax2)
ax3.plot(U_az[76, :])
# plt.show()



vmin = min(np.min(v_gaussian[frame, :, :]), np.min(u_gaussian[frame, :, :]))
vmax = max(np.max(v_gaussian[frame, :, :]), np.max(u_gaussian[frame, :, :]))
norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)


f2, ax = plt.subplots(2, 2, )
ax[0,0].plot(u_gaussian[frame, int(y_c), :])
ax[0,0].set_title("$du/dx$")
ax[0,1].contourf(u_gaussian[frame, :, :], cmap = 'seismic', norm = norm)
ax[0,1].set_title("u contour")
ax[1,0].plot(v_gaussian[frame, :, int(x_c)], label = "$dv/dy$")
ax[1,0].set_title("$dv/dy$")
ax[1,1].contourf(v_gaussian[frame, :, :], cmap = 'seismic', norm = norm)
ax[1,1].set_title("v contour")
plt.legend()


###Copy from Sam's code

# r, theta, U_r, U_az, x0, y0= oj.ConvertCylindrical(x_c, y_c, x, y, umean, vmean)
# r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(x_c, y_c, x, y, u_gaussian[frame,:,:], v_gaussian[frame,:,:])
r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(120, 75, x, y, u_gaussian[frame,:,:], v_gaussian[frame,:,:])
r_arr, theta_arr, U_rBins, U_azBins = oj.binCylindrical(r, theta, U_r, U_az, thetaBins=30, rBins=30)
inds = (r.flatten()).argsort()
r2 = (r.flatten())[inds]
U_az2 = (U_az.flatten())[inds]
p = np.poly1d(np.polyfit(r2, U_az2, 11))(r2)
max = np.argmax(p)


f3, ax3 = plt.subplots()
# ax3.scatter(r2*d, U_az2)
ax3.scatter(r2*d, p)
ax3.set_xlabel("$r/d$")
ax3.set_ylabel("$U_{az}$")
plt.show()