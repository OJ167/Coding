import numpy as np
import os
import sys
import mat73
from scipy.interpolate import make_interp_spline, BSpline
from scipy import io
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import pandas as pd
import matplotlib.colors as colors
import matplotlib.cm
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
from scipy.interpolate import RectBivariateSpline
import h5py
# from colorspacious import cspace_converter

#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)


####Import Ollie Tools MAC
# dirPath = "/Users/olliejackson/Coding"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)

##### Set plot style #####
plt.style.use(["science", "vibrant", "no-latex"])
cmap = plt.get_cmap("jet_r")



Rotations = ['RPM0', 'RPM1', 'RPM2', 'RPM3', 'RPM6', 'RPM9', 'RPM12']
Injection = ['U50', 'U100']
Stroke = ['L50', 'L100']
I = 'U100'
S = 'L50'
R = 'RPM9'

h5file = h5py.File('E:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)][str(S)][str(Rotations[6])]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
time = oj.frames_to_seconds(u, v, 90)


# track vorticity Old
VortLocMaxold, VortLocMinold = oj.vorticityPeakTracking(u, v)

EnstLocMaxold = oj.enstrophyPeakTracking(u, v)
EnstLocMaxnew = oj.enstrophyPeakTracking_inter(u, v)


f1, ax1 = plt.subplots()
# ax1.plot(VortLocMaxold[:,1], label = "Vortex Max Old")
# ax1.plot(VortLocMinold[:,1], label = "Vortex Min Old")
# ax1.plot(time, EnstLocMaxold[:,1], label = "Enstrophy Max Old")
ax1.plot(time, EnstLocMaxnew[:,1], c = 'b', label = "Enstrophy Max new")
plt.legend()
# plt.show()

# print(len(Rotations))

# uall = np.zeros([u.shape[0], u.shape[1], u.shape[2], len(Rotations)])
# vall = np.zeros([u.shape[0], u.shape[1], u.shape[2], len(Rotations)])

# for i in range(len(Rotations)):
#     vels = h5file['Narrow'][str(I)][str(S)][str(Rotations[i])]
#     u = vels[:,:,:,0]
#     v = vels[:,:,:,1]
#     uall[:,:,:,i] = u[:,:,:]
#     vall[:,:,:,i] = u[:,:,:]

# EnstLocMaxnew0  = oj.enstrophyPeakTracking_inter(uall[:,:,:,0], vall[:,:,:,0])
# EnstLocMaxnew1  = oj.enstrophyPeakTracking_inter(uall[:,:,:,1], vall[:,:,:,1])
# EnstLocMaxnew2  = oj.enstrophyPeakTracking_inter(uall[:,:,:,2], vall[:,:,:,2])
# EnstLocMaxnew3  = oj.enstrophyPeakTracking_inter(uall[:,:,:,3], vall[:,:,:,3])
# EnstLocMaxnew6  = oj.enstrophyPeakTracking_inter(uall[:,:,:,4], vall[:,:,:,4])
# EnstLocMaxnew9  = oj.enstrophyPeakTracking_inter(uall[:,:,:,5], vall[:,:,:,5])
# EnstLocMaxnew12 = oj.enstrophyPeakTracking_inter(uall[:,:,:,6], vall[:,:,:,6])


# f2, ax2 = plt.subplots()
# ax2.plot(time, EnstLocMaxnew0[:,1], label = '0RPM')
# ax2.plot(time, EnstLocMaxnew1[:,1], label = '1RPM ' )
# ax2.plot(time, EnstLocMaxnew2[:,1], label = '2RPM ' )
# ax2.plot(time, EnstLocMaxnew3[:,1], label = '3RPM ' )
# ax2.plot(time, EnstLocMaxnew6[:,1], label = '6RPM ' )
# ax2.plot(time, EnstLocMaxnew9[:,1], label = '9RPM ' )
# ax2.plot(time, EnstLocMaxnew12[:,1], label = '12RPM ')
# plt.legend()
# plt.show()


h5file = h5py.File('E:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow']['U50']['L50'][str(R)]
u5050 = vels[:,:,:,0]
v5050 = vels[:,:,:,1]

h5file = h5py.File('E:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow']['U100']['L50'][str(R)]
u10050 = vels[:,:,:,0]
v10050 = vels[:,:,:,1]

h5file = h5py.File('E:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow']['U50']['L100'][str(R)]
u50100 = vels[:,:,:,0]
v50100 = vels[:,:,:,1]

h5file = h5py.File('E:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow']['U100']['L100'][str(R)]
u100100 = vels[:,:,:,0]
v100100 = vels[:,:,:,1]


Enstu5050   = oj.enstrophyPeakTracking_inter(u5050,   v5050  )
Enstu10050  = oj.enstrophyPeakTracking_inter(u10050,  v10050 )
Enstu50100  = oj.enstrophyPeakTracking_inter(u50100,  v50100 )
Enstu100100 = oj.enstrophyPeakTracking_inter(u100100, v100100)

f2, ax2 = plt.subplots()
ax2.plot(time[80:], Enstu5050  [80:,1]  , label = 'U50 L50')
ax2.plot(time[80:], Enstu10050 [80:,1] , label = 'U100 L50')
ax2.plot(time[80:], Enstu50100 [80:,1] , label = 'U50 L100')
ax2.plot(time[80:], Enstu100100[80:,1], label = 'U100 L100')
plt.title(str(R) + " RPM")
plt.legend()
plt.show()