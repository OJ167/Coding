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

h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')

vels = h5file['Narrow']['U50']['L50']['RPM12']
u = vels[:,:,:,0]
v = vels[:,:,:,1]

umean = np.mean(u, axis=0)
vmean = np.mean(v, axis=0)

h5file.close()


f1, (ax1) = plt.subplots(nrows=1, ncols=1)
ax1.contourf(umean[:,:], cmap = "seismic")
plt.title("Velocity Contour")
plt.show()