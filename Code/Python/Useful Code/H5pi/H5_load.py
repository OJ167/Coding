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

h5file = h5py.File('E:/H5/meandataVLSFine.h5', 'r')
# h5file = h5py.File('E:/H5/3D0HLSFine.h5', 'r')

vels = h5file['Narrow']['U100']['L50']['RPM3']
# vels = h5file['3D0']['U100']['L100']['RPM12']
u = vels[:,:,:,0]
v = vels[:,:,:,1]

umean = np.mean(u, axis=0)
vmean = np.mean(v, axis=0)

frame = 500
u_gauss, v_gauss = gaussian_filter(u, sigma=0.7), gaussian_filter(v, sigma=0.7)

# descend_obj(h5file)
oj.descend_obj(h5file)
h5file.close()


f1, (ax1) = plt.subplots(nrows=1, ncols=1)
ax1.contourf(umean[:,:], cmap = "seismic")
plt.title("Velocity Contour")
# plt.show()


f1, (ax1) = plt.subplots(nrows=1, ncols=1)
ax1.contourf(u[200,:,:], cmap = "seismic")
plt.title("Axial Velocity Contour frame 300")








r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
f2, ax2 = plt.subplots(nrows=1, ncols=1)
ax2. quiver(z_nd, r_nd, u_gauss[frame,:,:], v_gauss[frame,:,:])



f3, ax3 = plt.subplots(nrows=1, ncols=1)
ax3.plot(u[100,80,:])
ax3.plot(u_gauss[100,:,32])




uProf_sav = np.zeros([u.shape[2]])
uProf_sav = savgol_filter(u[150,80,:] , 19, 2)
vProf_sav = np.zeros([v.shape[1]])
vProf_sav = savgol_filter(u_gauss[150,:,32], 19, 2)


f4, ax4 = plt.subplots(nrows=1, ncols=1)
ax4.plot(uProf_sav[:])
ax4.plot(vProf_sav[:])


f5, (ax5, ax6) = plt.subplots(ncols = 2)
ax5.quiver(z_nd, r_nd, u_gauss[frame,:,:], v_gauss[frame,:,:])
ax6.streamplot(z_nd, r_nd, u_gauss[frame,:,:], v_gauss[frame,:,:], color = 'b')

# im = plt.imread('G:/Testing/RPM-6.0__Upiston-100__Stroke-100/2023-08-18__FPS-90/3/B/00000499.tiff')
f6, ax7 = plt.subplots(nrows=1, ncols=1)
# ax7.imshow(im,extent=[ z_nd[0], z_nd[-1], r_nd[0], r_nd[-1]], cmap = 'Greys_r')
ax7.streamplot(z_nd, r_nd, u_gauss[frame,:,:], v_gauss[frame,:,:], color = 'b', broken_streamlines = False)
plt.show()


# Create a mask
mask = np.zeros(U.shape, dtype=bool)
mask[40:60, 40:60] = True
U[:20, :20] = np.nan
U = np.ma.array(U, mask=mask)


f7, ax8 = plt.subplots(nrows=1, ncols=1)
# ax8.imshow(im,extent=[ z_nd[0], z_nd[-1], r_nd[0], r_nd[-1]], cmap = 'Greys_r')
ax8.streamplot(z_nd, r_nd, u_gauss[frame,:,:], v_gauss[frame,:,:], color = 'b')