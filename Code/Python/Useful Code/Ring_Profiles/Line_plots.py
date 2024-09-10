import matplotlib.pyplot as plt
import numpy as np
import h5py
from scipy.signal import savgol_filter
import os
import sys
from scipy.ndimage import gaussian_filter
import matplotlib.cm
import matplotlib.colors as colors

#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)
plt.style.use(["science", "vibrant", "no-latex"])

from tkinter.filedialog import askdirectory

####Import Ollie Tools MAC
# dirPath = "/Users/olliejackson/Coding"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)

##### Set plot style #####
plt.style.use(["science", "vibrant", "no-latex"])
matplotlib.rc('xtick', labelsize=8) 
matplotlib.rc('ytick', labelsize=8) 

h5file = h5py.File('E:/H5/meandataVLSFine.h5', 'r')

vels = h5file['Narrow']['U100']['L50']['RPM0']
# vels = h5file['0D0']['U100']['L100']['RPM12']
u = vels[:,:,:,0]
v = vels[:,:,:,1]
h5file.close()

u, v = oj.importData73('F:/Testing/RPM-0.0__Upiston-100__Stroke-100/2023-08-22__FPS-90/2/Data/PIV_export_fine.mat')
u, v = oj.create_Mean(10, 'F:/Testing/RPM-0.0__Upiston-100__Stroke-100/2023-08-22__FPS-90/')

axial_distance = 51
frame = 150

uProf_sav = np.zeros([u.shape[1]])
uProf_sav = savgol_filter(u[frame,:,51] , 19, 2)
vProf_sav = np.zeros([v.shape[1]])
vProf_sav = savgol_filter(v[frame,:,51], 19, 2)

r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])


f1, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(5.5, 4))
ax1.contourf(z_nd, r_nd, u[frame,:,:], cmap = "seismic")
plt.title("Axial Velocity Contour frame {}".format(frame))

f2, ax2 = plt.subplots(nrows=1, ncols=1, figsize=(5.5, 4))
plt.title("Profile at y = 51")
ax2.plot(uProf_sav[:], 'o-', label = 'axial velocity')
ax2.plot(vProf_sav[:], 'o-', label = 'radial velocity')
ax2.legend()
plt.show()