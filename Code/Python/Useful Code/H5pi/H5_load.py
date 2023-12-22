import matplotlib.pyplot as plt
import numpy as np
import h5py
from scipy.signal import savgol_filter
import os
import sys

#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)
plt.style.use(["science", "vibrant", "no-latex"])

from tkinter.filedialog import askdirectory

def descend_obj(obj,sep='\t'):
    """
    Iterate through groups in a HDF5 file and prints the groups and datasets names and datasets attributes
    """
    if type(obj) in [h5py._hl.group.Group,h5py._hl.files.File]:
        for key in obj.keys():
            print(sep,'-',key,':',obj[key])
            descend_obj(obj[key],sep=sep+'\t')
    elif type(obj)==h5py._hl.dataset.Dataset:
        for key in obj.attrs.keys():
            print(sep+'\t','-',key,':',obj.attrs[key])

################ To load in. move this to another file 

# h5file = h5py.File('G:/H5/meandataVLS.h5', 'r')
h5file = h5py.File('F:/H5/3D0HLSFine.h5', 'r')

# vels = h5file['Narrow']['U100']['L100']['RPM12']
vels = h5file['3D0']['U100']['L100']['RPM12']
u = vels[:,:,:,0]
v = vels[:,:,:,1]

umean = np.mean(u, axis=0)
vmean = np.mean(v, axis=0)


descend_obj(h5file)


f1, (ax1) = plt.subplots(nrows=1, ncols=1)
ax1.contourf(umean[:,:], cmap = "seismic")
plt.title("Velocity Contour")
# plt.show()

# oj.descend_obj(h5file)
h5file.close()

f1, (ax1) = plt.subplots(nrows=1, ncols=1)
ax1.contourf(u[750,:,:], cmap = "seismic")
plt.title("Axial Velocity Contour frame 300")








r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
f2, ax2 = plt.subplots(nrows=1, ncols=1)
ax2. quiver(z_nd, r_nd, u[1000,:,:], v[1000,:,:])



f3, ax3 = plt.subplots(nrows=1, ncols=1)
ax3.plot(u[750,80,:])
ax3.plot(v[750,:,120])




uProf_sav = np.zeros([u.shape[2]])
uProf_sav = savgol_filter(u[750,80,:] , 19, 2)
vProf_sav = np.zeros([v.shape[1]])
vProf_sav = savgol_filter(v[750,:,120], 19, 2)


f4, ax4 = plt.subplots(nrows=1, ncols=1)
ax4.plot(uProf_sav[:])
ax4.plot(vProf_sav[:])
plt.show()