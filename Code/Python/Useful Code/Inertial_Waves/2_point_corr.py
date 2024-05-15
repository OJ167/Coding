
################################################################################################
####### Sam's unchanged at the top
################################################################################################

# import matplotlib.pyplot as plt
# import numpy as np
# import os
# import sys
# import scienceplots
# import h5py

# dirPath = os.getcwd()
# sys.path.insert(0, dirPath)
# import Tools as sb

# plt.style.use(["science", "vibrant"])
# plt.rcParams['figure.constrained_layout.use'] = True
# plt.rcParams['figure.figsize'] = (8, 6)
# plt.rcParams['figure.dpi'] = 180
# # cmap = plt.get_cmap("jet_r")

# fps = np.array([20, 20, 20, 30, 30], dtype=int)
# PRPM = np.array([2, 4, 8, 16, 32], dtype=int)
# vel0 = 0.01162 * PRPM / 2
# q0 = 0.000000329 * PRPM / 2

# rpm = np.array([5, 10, 20, 40])
# RealRpm = np.array((5.232, 10.164, 20.022, 39.744)) # 29.88,

# nRot = rpm.shape[0]
# nInj = PRPM.shape[0]

# d = 0.006

# h5file = h5py.File('/Users/sambooth/Library/Mobile Documents/com~apple~CloudDocs/Data/dataVLS.h5', 'r')

# ReArr       = np.zeros((nRot, nInj))
# RoArr       = np.zeros((nRot, nInj))
# EkArr       = np.zeros((nRot, nInj))

# mask = h5file['MISC']['Mask']
# ExX = mask.shape[1]
# ExY = mask.shape[0]
# proportion = ExY / ExX

# f1, ax1s = plt.subplots(nrows=1, ncols=1, figsize = (4, 5))

# r, z = sb.NDUnitsForPlots(ExX, ExY)
# X, Y = np.meshgrid(r, z)

# Angles = np.linspace(10, 80, dtype='int')
# # Angles= np.array([20, 30, 40, 50, 60, 70, 80])
# left = 31
# right = 53

# runRot = 1
# runInj = 1

# ## Import flow field 
# data = h5file['RPM{0}'.format(rpm[runRot])]['INJ{0}'.format(PRPM[runInj])]

# uTemp = data[:, :, : ,0] * mask #/ vel0[runInj]
# vTemp = data[:, :, : ,1] * mask #/ vel0[runInj]

# vmean = np.mean(vTemp, axis=0)
# angMean = np.zeros(Angles.shape[0])
# sb.tic()
# for i in range(Angles.shape[0]):
#     sb.progressBar(i, Angles.shape[0])
#     ang = Angles[i]

#     if ang == 60:
#         angMean[i] = 0 
#     else:
#         IWsF = sb.IWFilter(vTemp, ang, fps=fps[runInj], rpm = RealRpm[runRot], phase = 1)

#         _,_,_,_,_,_,angDL = sb.TwoPtCorrIWs(IWsF[:, 2:, :left])
#         _,_,_,_,_,_,angDR = sb.TwoPtCorrIWs(IWsF[:, 2:, right:])
#         angD = (angDL+angDR)/2
#         angMean[i] = angD
# angMean = sb.InterpZeros(angMean)

# sb.toc()
# h5file.close()

# FByOmega = 2 * np.cos(np.deg2rad(Angles)) 

# ax1s.plot(FByOmega, Angles, linestyle="dotted", color = 'black', label = 'Dispersion Relation')
# ax1s.plot(FByOmega, angMean, color='blue', linestyle="none", marker=".", markersize=5, alpha=0.75, label = 'Ek - {}'.format(np.round(sb.Ek(RealRpm[runRot]), 4)))
# ax1s.legend()

# plt.setp(ax1s, xlabel=r'$F_{f} / F_{\Omega}$')
# plt.setp(ax1s, ylabel=r"$\theta$  (deg)")

# # f1.savefig('/Users/sambooth/Desktop/Thesis Bits/Ch7/VLS_2PtSingle.png', bbox_inches='tight')

# plt.show()


######################################################################################
######### Ollie's changed version
######################################################################################

import matplotlib.pyplot as plt
import numpy as np
import os
import sys
# import scienceplots
import h5py

#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)
plt.style.use(["science", "vibrant", "no-latex"])

# h5file = h5py.File('E:/H5/meandataVLSFine.h5', 'r')
h5file = h5py.File('E:/H5/meandataVLS.h5', 'r')

Vels = ['U50', 'U100']
Len = ['L50', 'L100']
RPMs = ['RPM0' , 'RPM1', 'RPM2', 'RPM3' ,'RPM6', 'RPM9', 'RPM12']

vels = h5file['Narrow'][Vels[0]][Len[0]][RPMs[0]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]


plt.rcParams['figure.constrained_layout.use'] = True
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['figure.dpi'] = 180


fps = np.array([20, 20, 20, 30, 30], dtype=int)
PRPM = np.array([2, 4, 8, 16, 32], dtype=int)
vel0 = 0.01162 * PRPM / 2
q0 = 0.000000329 * PRPM / 2

rpm = np.array([0, 1, 2, 3, 6, 9, 12])
RealRpm = np.array([0, 1, 2, 3, 6, 9, 12]) # 29.88,

nRot = rpm.shape[0]
nInj = PRPM.shape[0]

d = 0.006

ReArr       = np.zeros((nRot, nInj))
RoArr       = np.zeros((nRot, nInj))
EkArr       = np.zeros((nRot, nInj))

# mask = h5file['MISC']['Mask']
# ExX = mask.shape[1]
# ExY = mask.shape[0]
# proportion = ExY / ExX

f1, ax1s = plt.subplots(nrows=1, ncols=1, figsize = (4, 5))

r, z = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
X, Y = np.meshgrid(r, z)

Angles = np.linspace(10, 80, dtype='int')
# Angles= np.array([20, 30, 40, 50, 60, 70, 80])
# left = 31
# right = 53
left  = 71
right = 73


runRot = 6
runInj = 1

## Import flow field 
# data = h5file['Narrow'][Vels[0]][Len[0]]['RPM{0}'.format(rpm[runRot])]
data = h5file['Narrow'][Vels[0]][Len[0]]['RPM12']
# data = h5file['RPM{0}'.format(rpm[runRot])]['INJ{0}'.format(PRPM[runInj])]

uTemp = data[:, :, : ,0] #* mask #/ vel0[runInj]
vTemp = data[:, :, : ,1] #* mask #/ vel0[runInj]

vmean = np.mean(vTemp, axis=0)
angMean = np.zeros(Angles.shape[0])
oj.tic()
for i in range(Angles.shape[0]):
    oj.progressBar(i, Angles.shape[0])
    ang = Angles[i]

    if ang == 60:
        angMean[i] = 0 
    else:
        IWsF = oj.IWFilter(vTemp, ang, fps=fps[runInj], rpm = RealRpm[runRot])#, phase = 1)
        # print(IWsF.shape)

        _,_,_,_,_,_,angDL = oj.TwoPtCorrIWs(IWsF[:, 2:, :left])
        _,_,_,_,_,_,angDR = oj.TwoPtCorrIWs(IWsF[:, 2:, right:])
        angD = (angDL+angDR)/2
        angMean[i] = angD
angMean = oj.InterpZeros(angMean)

oj.toc()
h5file.close()

FByOmega = 2 * np.cos(np.deg2rad(Angles)) 

ax1s.plot(FByOmega, Angles, linestyle="dotted", color = 'black', label = 'Dispersion Relation')
ax1s.plot(FByOmega, angMean, color='blue', linestyle="none", marker=".", markersize=5, alpha=0.75)#, label = 'Ek - {}'.format(np.round(sb.Ek(RealRpm[runRot]), 4)))
ax1s.legend()

plt.setp(ax1s, xlabel=r'$F_{f} / F_{\Omega}$')
plt.setp(ax1s, ylabel=r"$\theta$  (deg)")

# f1.savefig('/Users/sambooth/Desktop/Thesis Bits/Ch7/VLS_2PtSingle.png', bbox_inches='tight')

plt.show()