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
from scipy.ndimage.filters import gaussian_filter


#####Import Ollie Tools
dirPath = "C:/Coding/Code"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)

u,  v = oj.importData73("G:/Testing/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/8/Data/PIV_export.mat")
u_gaussian, v_gaussian = gaussian_filter(u, sigma=0.7), gaussian_filter(v, sigma=0.7)
r_nd, z_nd = oj.NDUnitsForPlotsWide(u.shape[1], u.shape[2])

time = oj.frames_to_seconds(u, v, 60)
f1, ax1 = plt.subplots(nrows=1, ncols=1)
ax1.set_title("Distribution of axial velocity")
ax1.plot(z_nd, u_gaussian[60,38,:]  , label = "1 Seconds")
ax1.plot(z_nd, u_gaussian[435,38,:] , label = "7.25 Seconds")
ax1.plot(z_nd, u_gaussian[810,38,:] , label = "13.5 Seconds")
ax1.plot(z_nd, u_gaussian[1185,38,:], label = "19.75 Seconds")
ax1.plot(z_nd, u_gaussian[1560,38,:], label = "26 Seconds")
plt.legend()
plt.show()



# u0,  v0 = oj.importData("F:/NozzleFOV/RPM-0__Upiston-100__Stroke-100/2022-11-24__FPS-30/1/Data/PIVlab.mat")
u0,  v0 = oj.importData73("F:/Testing/RPM-0.0__Upiston-50__Stroke-50/2023-05-25__FPS-90/1/Data/PIV_export.mat")
u0_gaussian, v0_gaussian = gaussian_filter(u0, sigma=0.7), gaussian_filter(v0, sigma=0.7)
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u0.shape[1], u0.shape[2])


f2, ax2 = plt.subplots(nrows=1, ncols=1)
ax2.set_title("Distribution of axial velocity")
ax2.plot(z_nd, u0_gaussian[int(1*90), 35, :]    , label = "1 Seconds")
ax2.plot(z_nd, u0_gaussian[int(7.25*90), 35, :] , label = "7.25 Seconds")
ax2.plot(z_nd, u0_gaussian[int(13.5*90), 35, :] , label = "13.5 Seconds")
ax2.plot(z_nd, u0_gaussian[int(19.75*90), 35, :], label = "19.75 Seconds")
ax2.plot(z_nd, u0_gaussian[int(26*90), 35, :]   , label = "26 Seconds")
plt.legend()
plt.show()

f3, ax3 = plt.subplots(nrows=1, ncols=1)
ax3.set_title("Distribution of axial velocity")
ax3.plot(z_nd, u0_gaussian[(1*90), 35 , :] ,   label = "1 Seconds")
ax3.plot(z_nd, u0_gaussian[(2*90), 35 , :] ,   label = "2 Seconds")
ax3.plot(z_nd, u0_gaussian[(3*90), 35 , :] ,   label = "3 Seconds")
ax3.plot(z_nd, u0_gaussian[(4*90), 35 , :] ,   label = "4 Seconds")
ax3.plot(z_nd, u0_gaussian[(5*90), 35 , :] ,   label = "5 Seconds")
plt.legend()
plt.show()




sampleT = [0, 6.25, 12.5, 18.75, 25]