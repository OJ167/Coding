import matplotlib.pyplot as plt
import numpy as np
import h5py

import os
import sys

#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)
plt.style.use(["science", "vibrant", "no-latex"])

from tkinter.filedialog import askdirectory


################ To load in. move this to another file 

# h5file = h5py.File('G:/H5/meandataVLS.h5', 'r')
h5file = h5py.File('F:/H5/3D0meandataHLS.h5', 'r')

# vels = h5file['Narrow']['U100']['L100']['RPM12']
vels = h5file['3D0']['U100']['L100']['RPM3']
u = vels[:,:,:,0]
v = vels[:,:,:,1]

umean = np.mean(u, axis=0)
vmean = np.mean(v, axis=0)



f1, (ax1) = plt.subplots(nrows=1, ncols=1)
ax1.contourf(umean[:,:], cmap = "seismic")
plt.title("Velocity Contour")
plt.show()

oj.descend_obj(h5file)
h5file.close()

f1, (ax1) = plt.subplots(nrows=1, ncols=1)
ax1.contourf(u[300,:,:], cmap = "seismic")
plt.title("Axial Velocity Contour frame 300")








r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
f2, ax2 = plt.subplots(nrows=1, ncols=1)
ax2. quiver(z_nd, r_nd, u[300,:,:], v[300,:,:])
plt.show()