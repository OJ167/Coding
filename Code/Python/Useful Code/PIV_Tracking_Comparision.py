import numpy as np
import os
import sys
import mat73
from scipy.interpolate import make_interp_spline, BSpline
from scipy import io
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
# from colorspacious import cspace_converter

#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)


##### Set plot style #####
plt.style.use(["science", "vibrant", "no-latex"])
cmap = plt.get_cmap("jet_r")

# u1,  v1  = oj.importData(f"G:/Testing/PIV_Comparison/PIVlab_GUI.mat")
# u2,  v2  = oj.importData73(f"G:/Testing/PIV_Comparison/PIV_export.mat")

u1,  v1  = oj.importData73(f"G:/Testing/RPM-0.0__Upiston-200__Stroke-100/2023-02-08__FPS-60/1/Data/PIV_export.mat") ### Original Images PIV data
u2,  v2  = oj.importData73(f"G:/Testing/Calibration files/Test_call/1/Data/PIV_export.mat") ### New Images PIV data - settigns are different

u1_gaussian,  v1_gaussian  = gaussian_filter(u1,  sigma=0.7), gaussian_filter(v1, sigma=0.7)
u2_gaussian,  v2_gaussian  = gaussian_filter(u2,  sigma=0.7), gaussian_filter(v2, sigma=0.7)

VortLocMax1, VortLocMin1 = oj.vorticityPeakTracking(u1_gaussian, v1_gaussian)
VortLocMax2, VortLocMin2 = oj.vorticityPeakTracking(u2_gaussian, v2_gaussian)

f1, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
plt.title("tracking rings with vorticity")
ax1.plot(VortLocMax1[:,1], label = "GUI")
ax2.plot(VortLocMax2[:,1], label = "Command")
plt.legend()
# plt.show()

vorticity1, vorticity_gaussian1 = oj.calculate_vorticity(u1, v1)
vorticity2, vorticity_gaussian2 = oj.calculate_vorticity(u2, v2)

f1, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
ax1.contourf(u1_gaussian[1100,:,:])
ax2.contourf(vorticity_gaussian1[1100,:,:])
plt.title("velocity vs vorticity at frame 1100")
# plt.show()


f1, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
ax1.contourf(u1[1100,:,:])
ax2.contourf(u2[1100,:,:])
plt.title("Velocity Contour GUI vs CMD")
plt.legend()
plt.show()

f1, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
ax1.contourf(u1_gaussian[1100,:,:])
ax2.contourf(u2_gaussian[1100,:,:])
plt.title("Velocity Contour  Gaussian GUI vs CMD")
plt.legend()
plt.show()

f1, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
ax1.contourf(vorticity1[1100,:,:])
ax2.contourf(vorticity2[1100,:,:])
plt.title("Vorticity Contour  Gaussian GUI vs CMD")
plt.legend()
plt.show()