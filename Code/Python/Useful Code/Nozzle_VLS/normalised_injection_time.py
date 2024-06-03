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

h5file = h5py.File('E:/H5/meandataVLSFine.h5', 'r')
# h5file = h5py.File('E:/H5/meandataVLS.h5', 'r')

Vels = ['U50', 'U100']
Len = ['L50', 'L100']
RPMs = ['RPM0' , 'RPM1', 'RPM2', 'RPM3' ,'RPM6', 'RPM9', 'RPM12']

vels = h5file['Narrow'][Vels[0]][Len[1]][RPMs[0]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
u, v = oj.scaleVelNozzle(u, v, 90)

VortLocMax, VortLocMin = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
Time = oj.frames_to_seconds(u, v, 90)


t_inj = 2.2
t_star = Time/t_inj
start_frame = 71
end_frame = 521 #for 5 seconds

end_frame_star = int(end_frame*t_inj)

VortLocMax5050, VortLocMin5050 = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
VortLocMin5050[:,0] = abs(np.subtract(VortLocMin5050[:,0], int(u.shape[1]/2)))
VortLocMax5050[:,0] = np.subtract(VortLocMax5050[:,0], int(u.shape[1]/2))
VortLocAvg5050 = np.zeros([VortLocMax5050.shape[0], 2])
VortLocAvg5050 = np.mean([VortLocMax5050, VortLocMin5050], axis = 0)


f1, ax1 = plt.subplots(nrows=1, ncols=1)
ax1.scatter(Time[:(end_frame-start_frame)],     VortLocAvg5050  [start_frame:end_frame,0], color='r', label = 'normal time')
ax1.scatter(t_star[:(end_frame_star-start_frame)],     VortLocAvg5050  [start_frame:end_frame_star,0], color='c', label = 't_star')
plt.legend()
plt.show()




####################### Normalised Injection Time #######################
# finding the injection time - maximum r value?

vort_max_temp = VortLocMax5050[start_frame:end_frame,0]
t_inj = np.argmax(vort_max_temp)
t_inj = t_inj / 90
t_star = Time/t_inj

f2, ax2 = plt.subplots(nrows=1, ncols=1)
ax2.scatter(Time[:(end_frame-start_frame)],     VortLocAvg5050  [start_frame:end_frame,0], color='r', label = 'normal time')
ax2.scatter(t_star[:(end_frame_star-start_frame)],     VortLocAvg5050  [start_frame:end_frame_star,0], color='c', label = 't_star')
plt.legend()
plt.show()


def normalise_injection_time(u, v, start_frame = 100, end_frame = 521):
    """
    normalise the time of the vortex ring by the time taken for the ring to be injected. 
    This looks at the maximum r value of the vortex ring and finds the time at which this occurs using the normal vortex tracking method.
    """

    VortLocMax, VortLocMin = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
    VortLocMin[:,0] = abs(np.subtract(VortLocMin[:,0], int(u.shape[1]/2)))
    VortLocMax[:,0] = np.subtract(VortLocMax[:,0], int(u.shape[1]/2))
    VortLocAvg = np.zeros([VortLocMax.shape[0], 2])
    VortLocAvg = np.mean([VortLocMax, VortLocMin], axis = 0)

    vort_max_temp = VortLocAvg[:,0]
    t_inj = np.argmax(vort_max_temp[start_frame:end_frame])
    t_inj = t_inj / 90
    end_frame_star = int(end_frame*t_inj)
    t_star = Time/t_inj
    print(t_inj)
    return t_star, end_frame_star

t_star, end_frame_star = normalise_injection_time(u, v)


print(len(t_star[:end_frame_star-start_frame]))
print(len(VortLocAvg5050  [start_frame:end_frame_star,0]))

f3, ax3 = plt.subplots(nrows=1, ncols=1)
ax3.scatter(Time[:(end_frame-start_frame)],     VortLocAvg5050  [start_frame:end_frame,0], color='r', label = 'normal time')
ax3.scatter(t_star[:(end_frame_star-start_frame)],     VortLocAvg5050  [start_frame:end_frame_star,0], color='c', label = 't_star')
plt.legend()
plt.show()





####### Comparing different injection conditions #################
index = 0

#5050
vels = h5file['Narrow']['U50']['L50'][RPMs[index]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
VortLocMax5050, VortLocMin5050 = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
VortLocMin5050[:,0] = abs(np.subtract(VortLocMin5050[:,0], int(u.shape[1]/2)))
VortLocMax5050[:,0] = np.subtract(VortLocMax5050[:,0], int(u.shape[1]/2))
VortLocAvg5050 = np.zeros([VortLocMax5050.shape[0], 2])
VortLocAvg5050 = np.mean([VortLocMax5050, VortLocMin5050], axis = 0)
t_star5050, end_frame_star5050 = normalise_injection_time(u, v)

#10050
vels = h5file['Narrow']['U100']['L50'][RPMs[index]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
VortLocMax10050, VortLocMin10050 = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
VortLocMin10050[:,0] = abs(np.subtract(VortLocMin10050[:,0], int(u.shape[1]/2)))
VortLocMax10050[:,0] = np.subtract(VortLocMax10050[:,0], int(u.shape[1]/2))
VortLocAvg10050 = np.zeros([VortLocMax10050.shape[0], 2])
VortLocAvg10050 = np.mean([VortLocMax10050, VortLocMin10050], axis = 0)
t_star10050, end_frame_star10050 = normalise_injection_time(u, v)

#50100
vels = h5file['Narrow']['U50']['L100'][RPMs[index]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
VortLocMax50100, VortLocMin50100 = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
VortLocMin50100[:,0] = abs(np.subtract(VortLocMin50100[:,0], int(u.shape[1]/2)))
VortLocMax50100[:,0] = np.subtract(VortLocMax50100[:,0], int(u.shape[1]/2))
VortLocAvg50100 = np.zeros([VortLocMax50100.shape[0], 2])
VortLocAvg50100 = np.mean([VortLocMax50100, VortLocMin50100], axis = 0)
t_star50100, end_frame_star50100 = normalise_injection_time(u, v)

#100100
vels = h5file['Narrow']['U100']['L100'][RPMs[index]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
VortLocMax100100, VortLocMin100100 = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
VortLocMin100100[:,0] = abs(np.subtract(VortLocMin100100[:,0], int(u.shape[1]/2)))
VortLocMax100100[:,0] = np.subtract(VortLocMax100100[:,0], int(u.shape[1]/2))
VortLocAvg100100 = np.zeros([VortLocMax100100.shape[0], 2])
VortLocAvg100100 = np.mean([VortLocMax100100, VortLocMin100100], axis = 0)
t_star100100, end_frame_star100100 = normalise_injection_time(u, v)

start_frame = 71
end_frame = 521 #for 5 seconds


f4, ax4 = plt.subplots(nrows=1, ncols=1)
plt.title('0 RPM Absolute Average Position of Vorticity Peaks in first 5 seconds normalised by injection time')
ax4.scatter(t_star5050[:(end_frame_star5050-start_frame)],     VortLocMax5050  [start_frame:end_frame_star5050,0], color='c', label = '50 50')
ax4.scatter(t_star10050[:(end_frame_star10050-start_frame)],     VortLocMax10050 [start_frame:end_frame_star10050,0], color='b', label = '100 50')
ax4.scatter(t_star50100[:(end_frame_star50100-start_frame)],     VortLocMax50100 [start_frame:end_frame_star50100,0], color='r', label = '50 100')
ax4.scatter(t_star100100[:(end_frame_star100100-start_frame)],     VortLocMax100100[start_frame:end_frame_star100100,0], color='g', label = '100 100')
ax4.set_ylim([22, 50])
ax4.set_xlabel(r'$t$[s]')
ax4.set_ylabel(r'$r$')
plt.legend()
plt.show()
