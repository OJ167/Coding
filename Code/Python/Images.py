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
# dirPath = "C:/Coding"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)
# plt.style.use(["science", "vibrant", "no-latex"])

from tkinter.filedialog import askdirectory

####Import Ollie Tools MAC
dirPath = "/Users/olliejackson/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)

##### Set plot style #####
# plt.style.use(["science", "vibrant", "no-latex"])
matplotlib.rc('xtick', labelsize=8) 
matplotlib.rc('ytick', labelsize=8) 


######## Pictures for Granny's Birthday ########

#### The one that looks like a flag
## Origninal image was vels = h5file['Narrow']['U100']['L50']['RPM12'], coarse data

# h5file = h5py.File('E:/H5/meandataVLSFine.h5', 'r')
# h5file = h5py.File('E:/H5/meandataVLS.h5', 'r')
h5file = h5py.File('/Volumes/HLS_0D0/H5/meandataVLSFine.h5', 'r')

vels = h5file['Narrow']['U100']['L50']['RPM12']

u = vels[:,:,:,0]
v = vels[:,:,:,1]

f1, ax1 = plt.subplots(nrows=1, ncols=1, layout="constrained", figsize = (7, 5))
ax1.axis("off")
ax1.contourf(u[500,:,:], cmap = 'seismic')
# f1.savefig('//cantus.ads.warwick.ac.uk/User44/u/u2088308/Documents/My Pictures/Gift_images/Coarseflag.png', dpi = 400)
# plt.show()

#### Long exposure in the right aspect ratio

# image = '//cantus.ads.warwick.ac.uk/User44/u/u2088308/Documents/My Pictures/longExposure/long-05032023185621-49.tiff'
# value = 7/5
# f1, ax1 = plt.subplots(nrows=1, ncols=1, layout="constrained", figsize = (7, 5))
# ax1.axis("off")
# ax1.imshow(plt.imread(image))
# f1.savefig('//cantus.ads.warwick.ac.uk/User44/u/u2088308/Documents/My Pictures/Gift_images/long_exposure.png', dpi = 400)
# plt.show()


####Streamline plot

# h5file = h5py.File('E:/H5/meandataVLSFine.h5', 'r')
# h5file = h5py.File('E:/H5/meandataVLS.h5', 'r')
h5file = h5py.File('/Volumes/HLS_0D0/H5/meandataVLSFine.h5', 'r')

vels = h5file['Narrow']['U100']['L100']['RPM0']

u = vels[:,:,:,0]
v = vels[:,:,:,1]

r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
z_nd_star = z_nd - 0.55
frame = 250

# im = plt.imread('C:/Users/u2088308/Pictures/image1_bg.tiff')
im = plt.imread('/Volumes/HLS_0D0/image1_bg.tiff')
f3, ax3 = plt.subplots(nrows=1, ncols=1, layout="constrained", figsize = (7, 5))
ax3.axis("off")
ax3.imshow(im,extent=[ z_nd_star[0], z_nd_star[-1], r_nd[0], r_nd[-1]], cmap = 'Greys_r')
ax3.streamplot(z_nd_star, r_nd, u[frame,:,:], v[frame,:,:], color = 'g', broken_streamlines = False, linewidth=0.5, arrowsize=0,)#, color=V[:,:])
# ax3.streamplot(r_nd, z_nd_star, np.rot90(-v[frame,:,:],1), np.rot90(u[frame,:,:],1),  color = 'g', arrowsize=0, linewidth=0.5)#, color=V[:,:])
ax3.set_xlim([z_nd_star[0], z_nd_star[-1]])
ax3.set_ylim([r_nd[0], r_nd[-1]])
ax3.grid(False)
# f3.savefig('//cantus.ads.warwick.ac.uk/User44/u/u2088308/Documents/My Pictures/Gift_images/0stream.png', dpi = 400)
plt.show()



#### Horizontal light sheet swirling velocity
# h5file = h5py.File('E:/H5/3D0HLSFine.h5', 'r')
h5file = h5py.File('E:/H5/3D0meandataHLS.h5', 'r')
vels = h5file['3D0']['U100']['L100']['RPM12']

frame = 1500

u = vels[:,:,:,0]
v = vels[:,:,:,1]
x = np.linspace(0 , u.shape[2], u.shape[2])
y = np.linspace(0 , u.shape[1], u.shape[1])
U_r  = np.zeros([u.shape[0], u.shape[1], u.shape[2]]) 
U_az = np.zeros([u.shape[0], u.shape[1], u.shape[2]])
X, Y = np.meshgrid(x, y) 

r, theta, U_r[frame,:,:], U_az[frame,:,:], x0, y0 = oj.ConvertCylindrical(int(u.shape[2]/2), int(u.shape[1]/2), x, y, u[frame,:,:], v[frame,:,:])

f4, ax4 = plt.subplots(nrows=1, ncols=1, layout="constrained", figsize = (7, 5))
ax4.axis("off")
ax4.contourf(X, Y, U_az[frame,:,:], cmap = "bwr")
ax4.quiver(X, Y, v[frame,:,:], u[frame,:,:])
# f4.savefig('//cantus.ads.warwick.ac.uk/User44/u/u2088308/Documents/My Pictures/Gift_images/HLS3.png', dpi = 400)
plt.show()