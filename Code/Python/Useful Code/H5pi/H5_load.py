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
# plt.style.use(["science", "vibrant", "no-latex"])

oj.thesis_plot_settings()

from tkinter.filedialog import askdirectory

####Import Ollie Tools MAC
# dirPath = "/Users/olliejackson/Coding"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)

##### Set plot style #####
# plt.style.use(["science", "vibrant", "no-latex"])
matplotlib.rc('xtick', labelsize=8) 
matplotlib.rc('ytick', labelsize=8) 

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

# h5file = h5py.File('E:/H5/meandataVLSFine.h5', 'r')
# h5file = h5py.File('E:/H5/3D0HLSFine.h5', 'r')
# h5file = h5py.File('F:/H5/0D0HLSFine.h5', 'r')
# h5file = h5py.File('E:/H5/LengthTest.h5', 'r')
# h5file = h5py.File('E:/H5/LengthTestNEW.h5', 'r')
h5file = h5py.File('E:/H5/WideFOV.h5', 'r')


# h5file = h5py.File('/Volumes/HLS_0D0/H5/3D0HLSFine.h5', 'r')
# h5file = h5py.File('/Volumes/HLS_0D0/H5/meandataVLSFine.h5')
# h5file = h5py.File('/Volumes/HLS_0D0/H5/LengthTestNEW.h5') #75 or 240
# h5file = h5py.File('/Volumes/HLS_0D0/H5/LengthTest.h5') #200

# vels = h5file['Narrow']['U100']['L75']['RPM0']
# vels = h5file['3D0']['U100']['L100']['RPM3']
vels = h5file['Wide']['U200']['L100']['RPM12']
u = vels[:,:,:,0]
v = vels[:,:,:,1]

umean = np.mean(u, axis=0)
vmean = np.mean(v, axis=0)

# u, v = oj.importData73('F:/Testing/RPM-0.0__Upiston-100__Stroke-100/2023-08-22__FPS-90/2/Data/PIV_export_fine.mat')
# u, v = oj.create_Mean(10, 'F:/Testing/RPM-0.0__Upiston-100__Stroke-100/2023-08-22__FPS-90/')

frame = 300
u_gauss, v_gauss = gaussian_filter(u, sigma=0.7), gaussian_filter(v, sigma=0.7)

r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])

# descend_obj(h5file)
oj.descend_obj(h5file)
h5file.close()


vmin = np.min(umean[:,:])
vmax = np.max(umean[:,:])
norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

f1, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(5.5, 3.5), layout="constrained")
ax1.contourf(z_nd, r_nd, umean[:,:], cmap = "bwr", norm=norm)
# ax1.imshow(umean[:,:], cmap = "seismic")
f1.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap="bwr"), ax=ax1, label = r'$\overline{u} ~[m/s]$')#, ax=ax1)
ax1.axhline(0, color = 'k', linestyle = '--', linewidth=0.5)
ax1.set_xlabel(r'$z/r{0}$')
ax1.set_ylabel(r'$r/r{0}$')
# f1.savefig('C:/Coding/umean75.png', dpi = 400)
# plt.title("Axial Velocity Contour")
# plt.show()


f1, (ax1) = plt.subplots(nrows=1, ncols=1)
ax1.contourf(z_nd, r_nd, u[frame,:,:], cmap = "seismic")
plt.title("Axial Velocity Contour frame {}".format(frame))








f2, ax2 = plt.subplots(nrows=1, ncols=1)
ax2. quiver(z_nd, r_nd, u_gauss[frame,:,:], v_gauss[frame,:,:])



f3, ax3 = plt.subplots(nrows=1, ncols=1)
ax3.plot(u[frame,35,:])
ax3.plot(u_gauss[frame,:,32])




uProf_sav = np.zeros([u.shape[2]])
uProf_sav = savgol_filter(u[frame,35,:] , 19, 2)
vProf_sav = np.zeros([v.shape[1]])
vProf_sav = savgol_filter(u_gauss[frame,:,51], 19, 2)


f4, ax4 = plt.subplots(nrows=1, ncols=1)
ax4.plot(uProf_sav[:])
ax4.plot(vProf_sav[:])


f5, (ax5, ax6) = plt.subplots(ncols = 2)
ax5.quiver(z_nd, r_nd, u_gauss[frame,:,:], v_gauss[frame,:,:])
ax6.streamplot(z_nd, r_nd, u_gauss[frame,:,:], v_gauss[frame,:,:], color = 'b')

# im = plt.imread('G:/Testing/RPM-6.0__Upiston-100__Stroke-100/2023-08-18__FPS-90/3/B/00000499.tiff')
f6, ax7 = plt.subplots(nrows=1, ncols=1)
# ax7.imshow(im,extent=[ z_nd[0], z_nd[-1], r_nd[0], r_nd[-1]], cmap = 'Greys_r')
ax7.streamplot(z_nd, r_nd, u_gauss[frame,:,:], v_gauss[frame,:,:], color = 'k')#, broken_streamlines = False)


V = np.sqrt(np.square(u_gauss[:,:,:]) + np.square(v_gauss[:,:,:]))

f7, ax8 = plt.subplots(nrows=1, ncols=1)
ax8.plot(V[frame,:,51])

# # Create a mask
# mask = np.zeros(U.shape, dtype=bool)
# mask[40:60, 40:60] = True
# U[:20, :20] = np.nan
# U = np.ma.array(U, mask=mask)


# f7, ax8 = plt.subplots(nrows=1, ncols=1)
# # ax8.imshow(im,extent=[ z_nd[0], z_nd[-1], r_nd[0], r_nd[-1]], cmap = 'Greys_r')
# ax8.streamplot(z_nd, r_nd, u_gauss[frame,:,:], v_gauss[frame,:,:], color = 'b')

# d = 0.1
# x = np.linspace(0 , umean.shape[1], umean.shape[1])
# y = np.linspace(0 , umean.shape[0], umean.shape[0])
# X, Y = np.meshgrid(x, y) 
# r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(120, 75, x, y, u[frame,:,:], v[frame,:,:])
# r_arr, theta_arr, U_rBins, U_azBins = oj.binCylindrical(r, theta, U_r, U_az, thetaBins=30, rBins=45)
# inds = (r.flatten()).argsort()
# r2 = (r.flatten())[inds]
# U_r2 = (U_r.flatten())[inds]
# pr = np.poly1d(np.polyfit(r2, U_r2, 11))(r2) #This turns the graph into a polynomial line

# f3, ax3 =plt.subplots()
# # ax3.scatter(r2*d, U_az2)
# plt.title(r"$U_{r}$ " + f"against Radius for frame {frame}")
# ax3.plot(r2*d, pr)
# ax3.set_xlabel("$r/d$")
# ax3.set_ylabel(r"$U_{r}$")




# r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(120, 75, x, y, u[frame,:,:], v[frame,:,:])
# r_arr, theta_arr, U_rBins, U_azBins = oj.binCylindrical(r, theta, U_r, U_az, thetaBins=30, rBins=45)
# inds = (r.flatten()).argsort()
# r2 = (r.flatten())[inds]
# U_az2 = (U_az.flatten())[inds]
# pf = np.poly1d(np.polyfit(r2, U_az2, 11))(r2) #This turns the graph into a polynomial line
# # max = np.argmax(p)
# max = np.max(pf)


# f3, ax3 =plt.subplots()
# # ax3.scatter(r2*d, U_az2)
# plt.title(r"$U_{az}$ " + f"against Radius for frame {frame}")
# ax3.plot(r2*d, pf)
# ax3.set_xlabel("$r/d$")
# ax3.set_ylabel(r"$U_{az}$")
f8, ax9 = plt.subplots(nrows=1, ncols=1)
plt.title("Profile at y = 51")
ax9.plot(u[frame,:,51], 'o-')
ax9.plot(v[frame,:,51], 'o-')
# plt.show()

divergence, divergence_gauss = oj.calculate_divergence(u, v)

f9, ax = plt.subplots(nrows=2, ncols=2)
ax[0,0].imshow(divergence_gauss[750,:,:], cmap = 'bwr')
ax[0,1].quiver(z_nd, r_nd, u_gauss[750,:,:], v_gauss[750,:,:])
ax[1,0].imshow(divergence_gauss[1350,:,:], cmap = 'bwr')
ax[1,1].quiver(z_nd, r_nd, u_gauss[1350,:,:], v_gauss[1350,:,:])
plt.show()