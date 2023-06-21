import numpy as np
import os
import sys
import mat73
from scipy.interpolate import make_interp_spline, BSpline
from scipy import io
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
import matplotlib.colors as colors



#####Import Ollie Tools
dirPath = "C:/Coding/Code"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)


######## Importing multiple rings #####
n = 10
u, v = oj.importData73("F:/Testing/RPM-0.0__Upiston-100__Stroke-50/2023-05-10__FPS-90/1/Data/PIV_export.mat")
# u, v = oj.importData73("")
u = np.zeros([n, u.shape[0], u.shape[1], u.shape[2]])
v = np.zeros([n, v.shape[0], v.shape[1], v.shape[2]])

for i in range(1, n+1):
    u[(i-1),:,:,:], v[(i-1),:,:,:] = oj.importData73(f"F:/Testing/RPM-0.0__Upiston-100__Stroke-50/2023-05-10__FPS-90/{i}/Data/PIV_export.mat")
    oj.progressBar(i, 10)

u_mean = np.mean(u, 0)
v_mean = np.mean(v, 0)

f1, (ax1, ax2) = plt.subplots(ncols=1, nrows=2, sharex=True, sharey=True)
for i in range(9):
    ax1.contourf(u[0, 500, :, :])
    ax2.contourf(u_mean[500, :, :])
# plt.show()

r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[2], u.shape[3])
x = np.linspace(0 , u_mean.shape[2], u_mean.shape[2])
y = np.linspace(0 , u_mean.shape[0], u_mean.shape[0])
X, Y = np.meshgrid(x, y)


Vmag_mean = np.sqrt(u_mean**2 + v_mean**2)
Vmag_mean = gaussian_filter(Vmag_mean, sigma=0.9)

f1, ax3 = plt.subplots(ncols=1, nrows=1, sharex=True, sharey=True)
ax3.contourf(z_nd, r_nd, Vmag_mean[500])
ax3.quiver(z_nd, r_nd, u_mean[500, :, :], v_mean[500, :, :])
# plt.show()


vorticity, vorticity_gauss = oj.calculate_vorticity(u_mean, v_mean)

f3, ax4 = plt.subplots(ncols=1, nrows=1, sharex=True, sharey=True)
ax4.contourf(z_nd, r_nd, vorticity_gauss[500], cmap = "bwr")
ax4.quiver(z_nd, r_nd, u_mean[500, :, :], v_mean[500, :, :])


f4, ax5 = plt.subplots(ncols=1, nrows=1, sharex=True, sharey=True)
ax5.contour(z_nd, r_nd, vorticity_gauss[500])
ax5.quiver(z_nd, r_nd, u_mean[500, :, :], v_mean[500, :, :])
plt.show()




oj.animate_cube_contourf(Vmag_mean, interval=11.1, cmap="bwr", save=0, output="15.mp4", fps=90, scale = 1, fsize = (12, 10))

oj.animate_cube_quiver(u_mean, v_mean, interval=11.1, cmap="bwr", save=0, output="15.mp4", fps=90, scale = 1, fsize = (12, 10))