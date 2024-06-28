import numpy as np
import sys as sys
import matplotlib.pyplot as plt
import h5py
from scipy.ndimage import gaussian_filter

#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)
# plt.style.use(["science", "vibrant", "no-latex"])
plt.style.use(["notebook", "vibrant", "no-latex"])

Dir = 'F:/Testing/RPM-0.0__Upiston-100__Stroke-100/2023-08-22__FPS-90/'
h5file = h5py.File('E:/H5/LengthTest.h5', 'r')

Vels = ['U100']
Len = ['L25', 'L50', 'L75', 'L100', 'L125', 'L150', 'L175', 'L200', 'L225', 'L240']
RPMs = ['RPM0']

vels = h5file['Narrow']['U100'][Len[0]]['RPM0']
u = vels[:,:,:,0]
v = vels[:,:,:,1]
u, v = oj.scaleVelNozzle(u, v, 90)
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])



data = u
stn_dev = np.std(data, axis = 2)


# f1, ax1 = plt.subplots(nrows=1, ncols=1)
# ax1.imshow(stn_dev, cmap = 'bwr')
# plt.show()



u, v = oj.load_multiple_rings(Dir, 10)

print(u.shape)
stn_dev = np.std(u[1:,:,:,:], axis = 0)
stn_dev = gaussian_filter(stn_dev, sigma = 1)
print(stn_dev.shape)

f2, ax = plt.subplots(nrows=2, ncols=2)
plt.suptitle('Standard Deviation of Axial Velocity')
ax[0,0].set_title('frame 0')
ax[0,0].imshow(stn_dev[0,:,:], cmap = 'bwr')
ax[0,1].set_title('frame 100')
ax[0,1].imshow(stn_dev[100,:,:], cmap = 'bwr')
ax[1,0].set_title('frame 500')
ax[1,0].imshow(stn_dev[500,:,:], cmap = 'bwr')
ax[1,1].set_title('frame 1000')
ax[1,1].imshow(stn_dev[1000,:,:], cmap = 'bwr')
plt.legend()
# plt.show()


f3, ax = plt.subplots(nrows=2, ncols=2)
plt.suptitle('Standard Deviation of Axial Velocity normlised by mean')
ax[0,0].set_title('frame 0')
ax[0,0].imshow(stn_dev[0,:,:]/np.mean(stn_dev[0,:,:]), cmap = 'bwr')
ax[0,1].set_title('frame 100')
ax[0,1].imshow(stn_dev[100,:,:]/np.mean(stn_dev[100,:,:]), cmap = 'bwr')
ax[1,0].set_title('frame 500')
ax[1,0].imshow(stn_dev[500,:,:]/np.mean(stn_dev[500,:,:]), cmap = 'bwr')
ax[1,1].set_title('frame 1000')
ax[1,1].imshow(stn_dev[1000,:,:]/np.mean(stn_dev[1000,:,:]), cmap = 'bwr')
plt.legend()

f4, ax = plt.subplots(nrows=2, ncols=2)
plt.suptitle('Standard Deviation of Axial Velocity normlised by maximum')
ax[0,0].set_title('frame 0')
ax[0,0].imshow(stn_dev[0,:,:]/np.max(stn_dev[0,:,:]), cmap = 'bwr')
ax[0,1].set_title('frame 100')
ax[0,1].imshow(stn_dev[100,:,:]/np.max(stn_dev[100,:,:]), cmap = 'bwr')
ax[1,0].set_title('frame 500')
ax[1,0].imshow(stn_dev[500,:,:]/np.max(stn_dev[500,:,:]), cmap = 'bwr')
ax[1,1].set_title('frame 1000')
ax[1,1].imshow(stn_dev[1000,:,:]/np.max(stn_dev[1000,:,:]), cmap = 'bwr')
plt.legend()
plt.show()