import numpy as np
import sys as sys
import matplotlib.pyplot as plt
import h5py
from scipy.ndimage import gaussian_filter
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
from matplotlib.ticker import LinearLocator

#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)
# plt.style.use(["science", "vibrant", "no-latex"])
plt.style.use(["notebook", "vibrant", "no-latex"])

# Dir = 'F:/Testing/RPM-0.0__Upiston-100__Stroke-100/2023-08-22__FPS-90/'
Dir = 'F:/Testing/RPM-12.0__Upiston-100__Stroke-50/2023-05-19__FPS-90/'
# Dir = 'F:/Testing/RPM-3.0__Upiston-100__Stroke-50/2023-05-15__FPS-90/'
h5file = h5py.File('E:/H5/LengthTest.h5', 'r')

Vels = ['U100']
Len = ['L25', 'L50', 'L75', 'L100', 'L125', 'L150', 'L175', 'L200', 'L225', 'L240']
RPMs = ['RPM0']

vels = h5file['Narrow']['U100'][Len[0]]['RPM0']
u = vels[:,:,:,0]
v = vels[:,:,:,1]
u, v = oj.scaleVelNozzle(u, v, 90)
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
z_nd = z_nd - 0.55
Time = oj.frames_to_seconds(u, v, 90)
print(z_nd.shape, r_nd.shape)


data = u
stn_dev = np.std(data, axis = 0)


# f1, ax1 = plt.subplots(nrows=1, ncols=1)
# ax1.imshow(stn_dev, cmap = 'bwr')
# plt.show()



# u, v = oj.load_multiple_rings(Dir, 10)

# print(u.shape)
# stn_dev = np.std(u[1:,:,:,:], axis = 0)
# stn_dev = gaussian_filter(stn_dev, sigma = 1)
# print(stn_dev.shape)

# f2, ax = plt.subplots(nrows=2, ncols=2)
# plt.suptitle('Standard Deviation of Axial Velocity')
# ax[0,0].set_title('frame 0')
# ax[0,0].imshow(stn_dev[0,:,:], cmap = 'bwr')
# ax[0,1].set_title('frame 100')
# ax[0,1].imshow(stn_dev[100,:,:], cmap = 'bwr')
# ax[1,0].set_title('frame 500')
# ax[1,0].imshow(stn_dev[500,:,:], cmap = 'bwr')
# ax[1,1].set_title('frame 1000')
# ax[1,1].imshow(stn_dev[1000,:,:], cmap = 'bwr')
# plt.legend()
# # plt.show()


# f3, ax = plt.subplots(nrows=2, ncols=2)
# plt.suptitle('Standard Deviation of Axial Velocity normlised by mean')
# ax[0,0].set_title('frame 0')
# ax[0,0].imshow(stn_dev[0,:,:]/np.mean(stn_dev[0,:,:]), cmap = 'bwr')
# ax[0,1].set_title('frame 100')
# ax[0,1].imshow(stn_dev[100,:,:]/np.mean(stn_dev[100,:,:]), cmap = 'bwr')
# ax[1,0].set_title('frame 500')
# ax[1,0].imshow(stn_dev[500,:,:]/np.mean(stn_dev[500,:,:]), cmap = 'bwr')
# ax[1,1].set_title('frame 1000')
# ax[1,1].imshow(stn_dev[1000,:,:]/np.mean(stn_dev[1000,:,:]), cmap = 'bwr')
# plt.legend()

# f4, ax = plt.subplots(nrows=2, ncols=2)
# plt.suptitle('Standard Deviation of Axial Velocity normlised by maximum')
# ax[0,0].set_title('frame 0')
# ax[0,0].imshow(stn_dev[0,:,:]/np.max(stn_dev[0,:,:]), cmap = 'bwr')
# ax[0,1].set_title('frame 100')
# ax[0,1].imshow(stn_dev[100,:,:]/np.max(stn_dev[100,:,:]), cmap = 'bwr')
# ax[1,0].set_title('frame 500')
# ax[1,0].imshow(stn_dev[500,:,:]/np.max(stn_dev[500,:,:]), cmap = 'bwr')
# ax[1,1].set_title('frame 1000')
# ax[1,1].imshow(stn_dev[1000,:,:]/np.max(stn_dev[1000,:,:]), cmap = 'bwr')
# plt.legend()






# # Make data.
# X = np.arange(0, 239, 1) #= z_nd
# Y = np.arange(0, 149, 1) #= r_nd 
# X, Y = np.meshgrid(z_nd, r_nd)


# ######### attempt at a 3d plot
# # z_nd, r_nd, stn_dev[:,:] = axes3d.get_test_data(0.05)

# f5, ax5 = plt.subplots(nrows=1, ncols=1, subplot_kw={'projection': '3d'})
# surface = ax5.plot_surface(X, Y, stn_dev[500,:,:], cmap = 'bwr')
# ax5.set_xlabel('$z/d$')
# ax5.set_ylabel('$r/d$')
# ax5.set_zlabel(r'$\sigma$')
# f5.colorbar(surface, shrink=0.5, aspect=5)
# f5.suptitle('Standard Deviation of Axial Velocity at frame 500')
# # plt.show()

# ##### Finding the time series of the maximum standard deviation per frame
# stn_dev_max = np.zeros(u.shape[1])
# for i in range(u.shape[1]):
#     stn_dev_max[i] = np.max(stn_dev[i,:,:])

# f6, ax6 = plt.subplots(nrows=1, ncols=1)
# ax6.plot(Time, stn_dev_max)
# ax6.set_xlabel('Time [s]')
# ax6.set_ylabel(r'$\sigma_{max}$')
# plt.show()


dirs_list = [
    'F:/Testing/RPM-0.0__Upiston-100__Stroke-100/2023-08-22__FPS-90/',
    'F:/Testing/RPM-1.0__Upiston-100__Stroke-100/2023-08-23__FPS-90/',
    'F:/Testing/RPM-2.0__Upiston-100__Stroke-100/2023-08-22__FPS-90/',
    'F:/Testing/RPM-3.0__Upiston-100__Stroke-100/2023-08-24__FPS-90/',
    'F:/Testing/RPM-6.0__Upiston-100__Stroke-100/2023-08-18__FPS-90/',
    'F:/Testing/RPM-9.0__Upiston-100__Stroke-100/2023-08-19__FPS-90/',
    'F:/Testing/RPM-12.0__Upiston-100__Stroke-100/2023-08-21__FPS-90/',
]

stn_dev_max = np.zeros([len(dirs_list), u.shape[0]])
print(stn_dev_max.shape)

for i in range(len(dirs_list)):
    u, v = oj.load_multiple_rings(dirs_list[i], 10)
    stn_dev = np.std(u[1:,:,:,:], axis = 0)
    stn_dev = gaussian_filter(stn_dev, sigma = 1)
    for j in range(u.shape[1]):
        stn_dev_max[i, j] = np.max(stn_dev[j,:,:])

f7, ax7 = plt.subplots(nrows=1, ncols=1)
ax7.plot(Time, stn_dev_max[0,:], label = '0 RPM')
ax7.plot(Time, stn_dev_max[1,:], label = '1 RPM')
ax7.plot(Time, stn_dev_max[2,:], label = '2 RPM')
ax7.plot(Time, stn_dev_max[3,:], label = '3 RPM')
ax7.plot(Time, stn_dev_max[4,:], label = '6 RPM')
ax7.plot(Time, stn_dev_max[5,:], label = '9 RPM')
ax7.plot(Time, stn_dev_max[6,:], label = '12 RPM')
ax7.set_xlabel('Time [s]')
ax7.set_ylabel(r'$\sigma_{max}$')
plt.legend()
plt.show()