#####
#
# Code to compare PIV output fields of old and new PIV analysis 20/11/2023 
#
#####




import numpy as np
import os
import sys
import mat73
import math as maths
from scipy.interpolate import make_interp_spline, BSpline
from scipy import io
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm
from scipy.ndimage import gaussian_filter


#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)

uold,  vold = oj.importData73("F:/Testing/RPM-0.0__Upiston-100__Stroke-100/2023-08-22__FPS-90/2/Data/PIV_export.mat")
uold,  vold = gaussian_filter(uold, sigma=0.7), gaussian_filter(vold, sigma=0.7)
r_ndold, z_ndold = oj.NDUnitsForPlotsWide(uold.shape[1], uold.shape[2])


unew,  vnew = oj.importData73("F:/Testing/RPM-0.0__Upiston-100__Stroke-100/2023-08-22__FPS-90/Small_window2/Data/PIV_export.mat")
unew,  vnew = gaussian_filter(unew, sigma=1.4), gaussian_filter(vnew, sigma=1.4)
r_ndnew, z_ndnew = oj.NDUnitsForPlotsWide(unew.shape[1], unew.shape[2])

f1, ax = plt.subplots(2,2, sharex=True,sharey=True)
ax[0,0].quiver(z_ndold, r_ndold, uold[200,:,:], vold[200,:,:])
ax[0,1].quiver(z_ndold, r_ndold, uold[400,:,:], vold[400,:,:])
ax[1,0].quiver(z_ndnew, r_ndnew, unew[200,:,:], vnew[200,:,:])
ax[1,1].quiver(z_ndnew, r_ndnew, unew[400,:,:], vnew[400,:,:])
ax[0,0].set_title("old velocity quiver frame 200")
ax[0,1].set_title("old velocity quiver frame 400")
ax[1,0].set_title("new velocity quiver frame 200")
ax[1,1].set_title("new velocity quiver frame 400")


f2, ax = plt.subplots(2,2,sharex=True,sharey=True)
ax[0,0].contourf(z_ndold, r_ndold, uold[200,:,:], cmap = "bwr")
ax[0,1].contourf(z_ndold, r_ndold, uold[400,:,:], cmap = "bwr")
ax[1,0].contourf(z_ndnew, r_ndnew, unew[200,:,:], cmap = "bwr")
ax[1,1].contourf(z_ndnew, r_ndnew, unew[400,:,:], cmap = "bwr")
ax[0,0].set_title("old axial velocity contour frame 200")
ax[0,1].set_title("old axial velocity contour frame 400")
ax[1,0].set_title("new axial velocity contour frame 200")
ax[1,1].set_title("new axial velocity contour frame 400")
# plt.show()


time = oj.frames_to_seconds(uold, uold, 90)

sumVorticityOld    = oj.sum_Vorticity(uold[:,:,18:], vold[:,:,18:])
sumVorticityNew    = oj.sum_Vorticity(unew[:,:,39:], vnew[:,:,39:])



f2, ax2 = plt.subplots(nrows=1, ncols=1)
plt.title("Vortex Ring Circulation 0 RPM")
ax2.plot(time, sumVorticityOld,   label = "OLD Speed 100, stroke: 100" )
ax2.plot(time, sumVorticityNew,   label = "NEW Speed 100, stroke: 100" )
ax2.set_xlabel("time [s]")
ax2.set_ylabel("$\Gamma \: [cm^{2}s^{-1}]$")
plt.legend()

f3, (ax3, ax4) = plt.subplots(nrows=2, ncols=1)
ax3.plot(r_ndold, uold[130, :, 15])
ax4.plot(r_ndnew, unew[130, :, 32])
plt.show()