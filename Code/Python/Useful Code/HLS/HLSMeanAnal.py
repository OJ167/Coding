import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import h5py


#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)
plt.style.use(["science", "vibrant", "no-latex"])
cmap = plt.get_cmap("jet_r")

fps = 150
PRPM = np.array([2, 4, 8, 16, 32, 64], dtype=int)
vel0 = 0.01162 * PRPM / 2
q0 = 0.000000329 * PRPM / 2

rpm = np.array([1, 2, 3, 6, 9, 12])
nRot = rpm.shape[0]
nInj = PRPM.shape[0]

d = 0.05

h5file = h5py.File('E:/H5/3D0meandataHLS.h5', 'r')

vels = h5file['3D0']['U100']['L100']['RPM3']
u = vels[:,:,:,0]
v = vels[:,:,:,1]

umean = np.mean(u, axis=0)
vmean = np.mean(v, axis=0)
x = 55
y = 35
x = np.linspace(0 , umean.shape[1], umean.shape[1])
y = np.linspace(0 , umean.shape[0], umean.shape[0])
X, Y = np.meshgrid(x, y) 

r, theta, U_r, U_az, x0, y0= oj.ConvertCylindrical(x, y, X, Y, umean, vmean)
r_arr, theta_arr, U_rBins, U_azBins = oj.binCylindrical(r, theta, U_r, U_az, thetaBins=5, rBins=5)


f1, ax1s = plt.subplots(nrows=nRot, ncols=nInj, sharex = 'all', sharey = 'all', layout='constrained')
f2, ax2s = plt.subplots(nrows=nRot, ncols=nInj, sharex = 'all', sharey = 'all', layout='constrained')
f21, ax21s = plt.subplots(nrows=nRot, ncols=nInj, sharex = 'all', sharey = 'all', layout='constrained')
f3, ax3s = plt.subplots(nrows=nRot, ncols=nInj, sharex = 'all', sharey = 'all', layout='constrained')
f4, ax4s = plt.subplots(nrows=nRot, ncols=nInj, sharex = 'all', sharey = 'all', layout='constrained')
f5, ax5 = plt.subplots(nrows = 1, ncols = 1, layout='constrained')

f6, ax6s = plt.subplots(nrows=nRot, ncols=nInj, sharex = 'all', sharey = 'all', layout='constrained')
f7, ax7s = plt.subplots(nrows=nRot, ncols=nInj, sharex = 'all', sharey = 'all', layout='constrained')


rMaxArr = np.zeros((nRot,nInj ))
uMaxArr = np.zeros((nRot,nInj ))


UseVort = np.ones((nInj, nRot))
UseVort[3, 0] = 0
UseVort[4, 0] = 0
UseVort[5, 0] = 0
UseVort[4, 1] = 0
UseVort[5, 1] = 0



for runRot in range(nRot):
    colorGen = cmap(float(runRot) / nRot)
    
    for runInj in range(nInj):
        vels0 = h5file['Upper']['RPM{0}'.format(rpm[runRot])]['INJ{0}'.format(PRPM[runInj])]
        Re_Temp = oj.Re(PRPM[runInj])
        umean = np.mean(vels0[:,:,:,0], axis=0)
        vmean = np.mean(vels0[:,:,:,1], axis=0)
        
        Xnd, Ynd = oj.NDUnitsForPlotsHoriz(vmean.shape[1], vmean.shape[0])
        X = Xnd * d
        Y = Ynd * d
        XndPlot, YndPlot = np.meshgrid(Xnd, Ynd)

        x, y, vort, vortSmooth = oj.find_vortex_center_Vorticity(umean, vmean, guass = 6, range = 10)
        if UseVort[runInj, runRot] == 0:
            x = 52.28
            y = 41.48

        
        r, theta, U_r, U_az, x0, y0= oj.ConvertCylindrical(x, y, X, Y, umean, vmean)
        
        r_arr, theta_arr, U_rBins, U_azBins = oj.binCylindrical(r, theta, U_r, U_az, thetaBins=5, rBins=5)

        inds = (r.flatten()).argsort()
        r2 = (r.flatten())[inds]
        U_az2 = (U_az.flatten())[inds]
        p = np.poly1d(np.polyfit(r2, U_az2, 11))(r2)
        max = np.argmax(p)

        rMaxArr[runRot, runInj] = rMax = r2[max]
        uMaxArr[runRot, runInj] = uMax = p[max]

        ax1s[runRot, runInj].set_title('Rot - {0}, Inj - {1}'.format(rpm[runRot], PRPM[runInj]))
        ax1s[runRot, runInj].quiver(XndPlot, YndPlot, umean, vmean)

        ax2s[runRot, runInj].set_title('Rot - {0}, Inj - {1}'.format(rpm[runRot], PRPM[runInj]))
        contf1 = ax2s[runRot, runInj].contourf(XndPlot, YndPlot, vort)#, vmin=-0.003, vmax=0.005, levels=11)
        
        ax21s[runRot, runInj].set_title('Rot - {0}, Inj - {1}'.format(rpm[runRot], PRPM[runInj]))
        ax21s[runRot, runInj].contourf(XndPlot, YndPlot, vortSmooth)
        ax21s[runRot, runInj].scatter(x0/d, y0/d)

        ax3s[runRot, runInj].set_title('Rot - {0}, Inj - {1}'.format(rpm[runRot], PRPM[runInj]))
        ax3s[runRot, runInj].scatter(r/d, U_az, color='c', alpha=0.5, edgecolors="k")
        ax3s[runRot, runInj].plot(r2/d, p, color='orange')

        ax4s[runRot, runInj].set_title('Rot - {0}, Inj - {1}'.format(rpm[runRot], PRPM[runInj]))
        ax4s[runRot, runInj].scatter(r/d, U_r, color='c', alpha=0.5, edgecolors="k")
        
        # ax5.scatter(rMax/d, uMax, alpha=0.5, color=colorGen)#color="k")
        ax5.annotate(str(np.round(Re_Temp)), (rMax/d, uMax))

        ax6s[runRot, runInj].plot(r_arr, np.mean(U_rBins, axis=1))

        ax7s[runRot, runInj].plot(r_arr, np.mean(U_azBins, axis = 1))

    ax5.plot(rMaxArr[runRot,:]/d, uMaxArr[runRot,:], color=colorGen, label = 'RPM - {}'.format(rpm[runRot]))

ax5.legend()

plt.setp(ax1s[:], xlabel=r"$x / d$")
plt.setp(ax1s[:], ylabel=r"$y / d$")

plt.setp(ax2s[:], xlabel=r"$x / d$")
plt.setp(ax2s[:], ylabel=r"$y / d$")
# f2.colorbar(contf1, ax=ax2s[:], location ='right')

plt.setp(ax2s[:], xlabel=r"$x / d$")
plt.setp(ax2s[:], ylabel=r"$y / d$")

plt.setp(ax3s[:], xlabel=r"$r/d$")
plt.setp(ax3s[:], ylabel=r"$U_{az}$")

plt.setp(ax4s[:], xlabel=r"$r/d$")
plt.setp(ax4s[:], ylabel=r"$U_{r}$")

ax5.set_xlabel(r"$r / d$")
ax5.set_ylabel(r"$U_{az, max}$")

plt.setp(ax6s[:], xlabel=r"$r/d$")
plt.setp(ax6s[:], ylabel=r"$U_{az}$")

plt.setp(ax7s[:], xlabel=r"$r/d$")
plt.setp(ax7s[:], ylabel=r"$U_{r}$")


h5file.close()

plt.show()