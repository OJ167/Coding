import matplotlib.pyplot as plt
import numpy as np
import h5py
from scipy.signal import savgol_filter
import os
import sys
from scipy.ndimage import gaussian_filter


#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)
plt.style.use(["science", "vibrant", "no-latex"])
oj.thesis_plot_settings()

h5file = h5py.File('E:/H5/meandataVLSFine.h5', 'r')
# h5file = h5py.File('E:/H5/meandataVLS.h5', 'r')

Vels = ['U50', 'U100']
Len = ['L50', 'L100']
RPMs = ['RPM0' , 'RPM1', 'RPM2', 'RPM3' ,'RPM6', 'RPM9', 'RPM12']

vels = h5file['Narrow'][Vels[0]][Len[0]][RPMs[0]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
u, v = oj.scaleVelNozzle(u, v, 90)

VortLocMax, VortLocMin = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
Time = oj.frames_to_seconds(u, v, 90)

start_frame = 71
start_frame = 71
end_frame = 521 #for 5 seconds

# f1, ax1 = plt.subplots(nrows=1, ncols=1)
# ax1.scatter(VortLocMax[91:2000,1], VortLocMax[91:2000,0], label = 'Max')
# ax1.scatter(VortLocMin[91:2000,1], VortLocMin[91:2000,0], label = 'Min')
# plt.legend()
# plt.show()



def convolved_derivitive(y, x, len = 15): 
    '''
    Convolved derivitive of a function dy/dx with length len coresponing to the number of points to average over
    len must be odd
    '''
    filt = np.ones(len)/len
    # print(len)
    # print(filt)
    y_smooth = np.convolve(y, filt, mode='valid')
    # dysdx = np.gradient(y_smooth, x[5:-5])
    # print(len/2, " = len/2")
    # print(int(len/2), " = int len/2")
    dysdx = np.gradient(y_smooth, x[int(len/2):-int(len/2)])

    return dysdx


drdt = np.gradient(VortLocMax[:,0])

drsdt = convolved_derivitive(VortLocMax[108:,0], Time[108:], 15)

print(drsdt.shape)
print('drsdt position 57 = ', drsdt[58])

f2, ax2 = plt.subplots(nrows=1, ncols=1)
plt.title('Ring Expansion Rate')
ax2.plot(VortLocMax[start_frame:end_frame,0]-95, label = 'Max')
ax2.plot(drdt [start_frame:end_frame], label = 'dr/dt')
# ax2.plot(drsdt[start_frame-int(15/2):end_frame], label = 'drs/dt')
ax2.plot(drsdt[:end_frame]-95, label = 'drs/dt')
plt.legend()
# plt.show()





########### Force the location to be at the nozzle before generation

VortLocMax[0:108,0] = 105 #####forcing the radial positon of the core to be at the nozzle (approximately) for the first 108 frames



drdt = np.gradient(VortLocMax[:,0])

drsdt = convolved_derivitive(VortLocMax[:,0], Time[:], 35)

print('drsdt position 57 = ', drsdt[58])

f2, ax2 = plt.subplots(nrows=1, ncols=1)
plt.title('Ring Expansion Rate - forcing start position')
ax2.plot(Time[:(end_frame-start_frame)], VortLocMax[start_frame:end_frame,0]-95, label = 'Max')
ax2.plot(Time[:(end_frame-start_frame)], drdt [start_frame:end_frame], label = 'dr/dt')
ax2.plot(Time[start_frame-int(35/2):end_frame], drsdt[start_frame-int(35/2):end_frame], label = 'drs/dt')
ax2.plot(Time[start_frame-int(35):end_frame]-0.534, drsdt[start_frame-int(35):end_frame], label = 'drs/dt aligned')
ax2.plot()
ax2.set_xlabel(r'$t$[s]')
# ax2.plot(drsdt[start_frame:end_frame], label = 'drs/dt')
plt.legend()
plt.show()


import numpy as np

# Sample data
x = np.linspace(0, 10, 100)
y = np.sin(x) + np.random.randn(100) * 0.1

# Define a smoothing kernel
kernel_size = 25
kernel = np.ones(kernel_size) / kernel_size

# Smooth the signal
smoothed_y = np.convolve(y, kernel, mode='same')

# Calculate the derivative of the smoothed signal
dy_dx = np.gradient(smoothed_y)

# Shift the smoothed signal to align with the derivative
offset = kernel_size // 2
shifted_smoothed_y = np.roll(smoothed_y, offset)

# Plot the original, smoothed, and shifted signals
plt.plot(x, y, label='Original')
plt.plot(x, smoothed_y, label='Smoothed')
plt.plot(x, shifted_smoothed_y, label='Shifted Smoothed')
plt.plot(x, dy_dx, label='Derivative')
plt.legend()
plt.show()