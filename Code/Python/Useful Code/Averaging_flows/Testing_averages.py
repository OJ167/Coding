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


vmax = np.max(u_mean)
vmin = np.min(u_mean)
norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)
f1, ax3 = plt.subplots(ncols=1, nrows=1, sharex=True, sharey=True)
ax3.contourf(z_nd, r_nd, u_mean[500], cmap = "seismic", norm = norm)
ax3.quiver(z_nd, r_nd, u_mean[500, :, :], v_mean[500, :, :])
# plt.show()


vorticity, vorticity_gauss = oj.calculate_vorticity(u_mean, v_mean)

f3, ax4 = plt.subplots(ncols=1, nrows=1, sharex=True, sharey=True)
ax4.contourf(z_nd, r_nd, vorticity_gauss[500], cmap = "bwr")
ax4.quiver(z_nd, r_nd, u_mean[500, :, :], v_mean[500, :, :])


f4, ax5 = plt.subplots(ncols=1, nrows=1, sharex=True, sharey=True)
ax5.contour(z_nd, r_nd, vorticity_gauss[500])
ax5.quiver(z_nd, r_nd, u_mean[500, :, :], v_mean[500, :, :])
# plt.show()




oj.animate_cube_contourf(Vmag_mean, interval=11.1, cmap="bwr", save=0, output="15.mp4", fps=90, scale = 1, fsize = (12, 10))

u_mean9 = np.mean(u[1:], 0)
u[0,:,:,:] = 10* u[0,:,:,:]
u_meanSkew = np.mean(u, 0)

f5, (ax6, ax7, ax8, ax9) = plt.subplots(ncols=1, nrows=4, sharex=True, sharey=True)
plt.suptitle("first ring, mean of other 9, mean of all, skewed mean")
ax6.contourf(z_nd, r_nd, u[0, 100, :, :])
ax7.contourf(z_nd, r_nd, u_mean9[100, :, :])
ax8.contourf(z_nd, r_nd, u_mean[100, :, :])
ax9.contourf(z_nd, r_nd, u_meanSkew[100, :, :])
plt.show()



#### squaring and maintainging argument test ####


original_array = np.array([3, -4, 5, -6])

# Square the original array
squared_array = np.square(original_array)

# Apply the modulus to the squared array
result_array = np.multiply(np.sign(original_array), squared_array)

print(result_array)

V_new = np.sqrt((np.multiply(np.sign(u), np.square(u))) + (np.multiply(np.sign(v), np.square(v))))

V_old = np.sqrt(u**2 + v**2)

f6, (ax10, ax11) = plt.subplots(ncols=1, nrows=2, sharex=True, sharey=True)
ax10.contourf(V_new[1,100,:,:])
ax11.contourf(V_old[1,100,:,:])
plt.suptitle("New vs Old Magnitude")
plt.show()

correlation_coefficient = np.corrcoef(u[1,100,:,:], u[2,100,:,:])[0, 1]
print("The correlation coefficient is:", correlation_coefficient)

for i in range(u.shape[0]):
    correlation_coefficient = np.corrcoef(u_mean9[300,:,:], u[3,300,:,:])[0, 1]
    print(f"Correlation coefficient {i}:", correlation_coefficient)


correlation_coefficient = np.corrcoef(u_mean9[300,:,:], u[3,300,:,:])[0, 1]
print(f"Correlation coefficient 3:", correlation_coefficient)

correlation_coefficient = np.corrcoef(u[3,300,:,:], u[4,300,:,:])[0, 1]
print(f"Correlation coefficient 3-4:", correlation_coefficient)

correlation_coefficient = np.corrcoef(u[:,300, 35, 56])
print(f"Correlation coefficient point:", correlation_coefficient)