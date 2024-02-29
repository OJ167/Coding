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
import timeit

#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)



uGUI, vGUI =   oj.importData("G:/Testing/RPM-6.0__Upiston-50__Stroke-50/2023-05-23__FPS-90/1/Data/PIVlab_GUI.mat")
uCMD, vCMD = oj.importData73("G:/Testing/RPM-6.0__Upiston-50__Stroke-50/2023-05-23__FPS-90/4/Data/PIV_export.mat")
# u0, v0 = oj.importData73("F:/Testing/RPM-0.0__Upiston-50__Stroke-50/2023-05-25__FPS-90/4/Data/PIV_export.mat")
# u3, v3 = oj.importData73("F:/Testing/RPM-3.0__Upiston-50__Stroke-50/2023-05-23__FPS-90/4/Data/PIV_export.mat")
# u6, v6 = oj.importData73("F:/Testing/RPM-6.0__Upiston-50__Stroke-50/2023-06-07__FPS-90/4/Data/PIV_export.mat")
# u9, v9 = oj.importData73("F:/Testing/RPM-9.0__Upiston-50__Stroke-50/2023-05-24__FPS-90/4/Data/PIV_export.mat")

u0, v0 = oj.importData73("G:/Testing/RPM-0.0__Upiston-100__Stroke-50/2023-05-10__FPS-90/4/Data/PIV_export.mat")
u3, v3 = oj.importData73("G:/Testing/RPM-3.0__Upiston-100__Stroke-50/2023-05-15__FPS-90/4/Data/PIV_export.mat")
u6, v6 = oj.importData73("G:/Testing/RPM-6.0__Upiston-100__Stroke-50/2023-05-11__FPS-90/4/Data/PIV_export.mat")
u9, v9 = oj.importData73("G:/Testing/RPM-9.0__Upiston-100__Stroke-50/2023-05-12__FPS-90/4/Data/PIV_export.mat")

r_ndGUI, z_ndGUI = oj.NDUnitsForPlotsNozzle(uGUI.shape[1], uGUI.shape[2])
r_ndCMD, z_ndCMD = oj.NDUnitsForPlotsNozzle(uCMD.shape[1], uCMD.shape[2])

vmin = min(np.min(uGUI), np.min(uCMD))
vmax = max(np.max(uGUI), np.max(uCMD))
norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

print("GUI max and min")
print(np.max(uGUI), np.min(uGUI))
print("CMD max and min")
print(np.max(uCMD), np.min(uCMD))
print("0RPM max and min")
print(np.max(u0), np.min(u0))
print("3RPM max and min")
print(np.max(u3), np.min(u3))
print("6RPM max and min ")
print(np.max(u6), np.min(u6))
print("9RPM max and min")
print(np.max(u9), np.min(u9))

f1, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True)
f1.suptitle("frame 200 axial velocity GUI top, CMD bottom")
ax1.contourf(z_ndGUI, r_ndGUI,uGUI[250,:,:], norm=norm, pivot = "middle", cmap = "bwr")
ax2.contourf(z_ndCMD, r_ndCMD,uCMD[250,:,:], norm=norm, pivot = "middle", cmap = "bwr")
f1.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap="bwr"), ax=ax1)
plt.show()

f2, ax3 = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
ax3.plot(z_ndCMD[18:], gaussian_filter(  u0[350,35,18:], sigma=0.7), label = "0RPM")
ax3.plot(z_ndCMD[18:], gaussian_filter(  u3[350,35,18:], sigma=0.7), label = "3RPM")
ax3.plot(z_ndCMD[18:], gaussian_filter(uCMD[350,35,18:], sigma=0.7), label = "6RPM OLD")
ax3.plot(z_ndCMD[18:], gaussian_filter(  u6[350,35,18:], sigma=0.7), label = "6RPM NEW")
ax3.plot(z_ndCMD[18:], gaussian_filter(  u9[350,35,18:], sigma=0.7), label = "9RPM")
plt.tight_layout()
plt.legend()
plt.show()

