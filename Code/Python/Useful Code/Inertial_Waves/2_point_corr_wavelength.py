import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import scienceplots
import h5py
dirPath = os.getcwd()
sys.path.insert(0, dirPath)
import OllieTools as oj

plt.style.use(["science", "vibrant"])
plt.rcParams['figure.constrained_layout.use'] = True
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['figure.dpi'] = 180
cmap = plt.get_cmap("jet_r")

fps = np.array([20, 20, 20, 30, 30], dtype=int)
PRPM = np.array([2, 4, 8, 16, 32], dtype=int)
vel0 = 0.01162 * PRPM / 2
q0 = 0.000000329 * PRPM / 2

rpm = np.array([5, 10, 20, 40])
RealRpm = np.array((5.232, 10.164, 20.022, 39.744)) # 29.88,

nRot = rpm.shape[0]
nInj = PRPM.shape[0]

d = 0.006

h5file = h5py.File('/Users/sambooth/Library/Mobile Documents/com~apple~CloudDocs/Data/dataVLS.h5', 'r')

ReArr       = np.zeros((nRot, nInj))
RoArr       = np.zeros((nRot, nInj))
EkArr       = np.zeros((nRot, nInj))

mask = h5file['MISC']['Mask']
ExX = mask.shape[1]
ExY = mask.shape[0]
proportion = ExY / ExX

f1, ax1s = plt.subplots(nrows=1, ncols=1, figsize = (4, 5))
f2, ax2s = plt.subplots(nrows=1, ncols=1, figsize = (6, 4))
f3, ax3s = plt.subplots(nrows=1, ncols=1, figsize = (6, 4))

r, z = oj.NDUnitsForPlots(ExX, ExY)
X, Y = np.meshgrid(r, z)

Angles = np.linspace(10, 80, dtype='int')
# Angles= np.array([20, 30, 40, 50, 60, 70, 80])
left = 31
right = 53

runRot = 2
runInj = 2

## Import flow field 
data = h5file['RPM{0}'.format(rpm[runRot])]['INJ{0}'.format(PRPM[runInj])]

uTemp = data[:, :, : ,0] * mask #/ vel0[runInj]
vTemp = data[:, :, : ,1] * mask #/ vel0[runInj]

vmean = np.mean(vTemp, axis=0)
angMean = np.zeros(Angles.shape[0])
distArray = np.zeros(Angles.shape[0])
FFArray = np.zeros(Angles.shape[0])

oj.tic()
for i in range(Angles.shape[0]):
    oj.progressBar(i, Angles.shape[0])
    ang = Angles[i]
    FFArray = oj.FiltFreqCalc(ang, RealRpm[runRot])

    if ang == 60:
        angMean[i] = 0 
        distArray[i] = 0 
    else:
        IWsF = oj.IWFilter(vTemp, ang, fps=fps[runInj], rpm = RealRpm[runRot], phase = 1)

        _,_,_,_,XCL,YCL,angDL = oj.TwoPtCorrIWs(IWsF[:, 2:, :left])
        _,_,_,_,XCR,YCR,angDR = oj.TwoPtCorrIWs(IWsF[:, 2:, right:])
        wlL = XCL * YCL / (np.sqrt(XCL**2 + YCL**2))
        wlR = XCR * YCR / (np.sqrt(XCR**2 + YCR**2))
        distArray[i] =  2 * (wlL + wlR) * 0.268/ ExX
        angD = (angDL+angDR)/2
        angMean[i] = angD

angMean = oj.InterpZeros(angMean)
distArray = oj.InterpZeros(distArray)

oj.toc()
h5file.close()

FByOmega = 2 * np.cos(np.deg2rad(Angles)) 

ax1s.plot(FByOmega, Angles, linestyle="dotted", color = 'black', label = 'Dispersion Relation')
ax1s.plot(FByOmega, angMean, color='blue', linestyle="none", marker=".", markersize=5, alpha=0.75, label = 'Ek - {}'.format(np.round(oj.Ek(RealRpm[runRot]), 4)))
ax1s.legend()

ax2s.plot(FByOmega, distArray, color='blue', linestyle="none", marker=".", markersize=5, alpha=0.75,)

plt.setp(ax1s, xlabel=r'$F_{f} / F_{\Omega}$')
plt.setp(ax1s, ylabel=r"$\theta$  (deg)")

plt.setp(ax2s, xlabel=r'$F_{f} / F_{\Omega}$')
plt.setp(ax2s, ylabel=r"$\lambda$ (m)")

# f1.savefig('/Users/sambooth/Desktop/Thesis Bits/Ch7/VLS_2PtSingle.png', bbox_inches='tight')

plt.show()
