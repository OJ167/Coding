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

h5file = h5py.File('E:/H5/LengthTest.h5', 'r')

Vels = ['U100']
Len = ['L25', 'L50', 'L75', 'L100', 'L125', 'L150', 'L175', 'L200', 'L225', 'L240',]
RPMs = ['RPM0']

vels = h5file['Narrow']['U100'][Len[0]]['RPM0']
u = vels[:,:,:,0]
v = vels[:,:,:,1]
u, v = oj.scaleVelNozzle(u, v, 90)

VortLocMax, VortLocMin = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
Time = oj.frames_to_seconds(u, v, 90)


for i in range(len(Len)):
    print(Len[i])
    item_name = f"L_{i}"
    user_input = input(f"Enter value for {item_name}: ")
    # No need to create a new variable, just assign the new information
    item_name = user_input  # Overwrite the previous value
    
