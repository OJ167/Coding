import matplotlib.pyplot as plt
import numpy as np

import os
import sys

# dirPath = os.getcwd()
# sys.path.insert(0, dirPath)
# import Tools as sb

# plt.style.use(['science','vibrant', 'no-latex'])

import cv2
import glob
from scipy import ndimage
import concurrent.futures
from scipy.fft import fft2,fftshift, ifft2

 

def draw_cicle(shape, diameter):
    """
    Input:
    shape    : tuple (height, width)
    diameter : scalar

    Output:
    np.array of shape  that has value 1 within a circle with diameter =  around center
    """
    assert len(shape) == 2
    TF = np.zeros(shape)  # ,dtype=np.bool)
    center = np.array(TF.shape) / 2.0
    XYRatio = shape[1] / shape[0]
    for iy in range(shape[0]):
        for ix in range(shape[1]):
            TF[iy, ix] = (int((iy - center[0]))) ** 2 + (int((ix - center[1])/XYRatio)) ** 2 < diameter**2
    TF = np.abs(TF - 1)
    return TF

def LowPass2D(Im, Circle, FiltStrength = 4):
    # 100, 5 for background lightsheet
    FFT1 = fft2(Im)
    FiltFFT = fftshift(FFT1)
    RemovedFFT = FiltFFT * Circle
    InvFFT = np.abs(ifft2(RemovedFFT))
    Subtracted = Im - InvFFT
    Guass = ndimage.gaussian_filter(Subtracted, FiltStrength)
    return Guass

FPS = 25
frameStart = 60
frameEnd = 350
totalFrames = frameEnd - frameStart

frame_slicer3001 = 50

nums = [int(0.1*totalFrames), int(0.3*totalFrames), int(0.5*totalFrames), int(0.7*totalFrames)]
length = int(len(nums))

Dir = 'E:\Repeatibility/3RPM\Ring1_3RPM\Side/*'
FileList = sorted(glob.glob(Dir)) [frameStart:frameEnd] #specific frames desired (start:stop:step)
col = 1
Im0 = cv2.imread(FileList[0])
Im0 = Im0[:,frame_slicer3001:]
print(Im0.shape)
Circle = draw_cicle((Im0.shape[0], Im0.shape[1]), 100)
Im0Cv = cv2.cvtColor(Im0, cv2.COLOR_BGR2RGB)
Im0filt = LowPass2D(Im0Cv[:,:,col], Circle)
COMTotal = np.zeros((2, length))
ImPro = np.zeros((Im0.shape[0], Im0.shape[1], length))
print('LOADED')


for n in range(len(nums)):
    ImTmp = cv2.imread(FileList[nums[n]])
    ImTmp = ImTmp[:,frame_slicer3001:]
    print(FileList[nums[n]])
    ImTmpCv = cv2.cvtColor(ImTmp, cv2.COLOR_BGR2RGB)
    ImTmpfilt = LowPass2D(ImTmpCv[:,:,col], Circle)
    ImTmpTest = np.abs(ImTmpfilt - Im0filt)
    mean = 20*np.mean(ImTmpTest)
    ImTmpTest[ImTmpTest < mean] = 0
    ImPro[:,:,n] = ImTmpTest 
    if np.any(ImTmpTest > 0)  == True:
        COMTotal[:,n] = ndimage.measurements.center_of_mass(ImTmpTest)
    else:
        COMTotal[:,n] = 0


plot1Time = str(int(0.1*totalFrames)/FPS)
plot1frames = str(0.1*totalFrames)
plot2Time = str(int(0.3*totalFrames)/FPS)
plot2frames = str(0.3*totalFrames)
plot3Time = str(int(0.5*totalFrames)/FPS)
plot3frames = str(0.5*totalFrames)
plot4Time = str(int(0.7*totalFrames)/FPS)
plot4frames = str(0.7*totalFrames)

f1, ((ax11, ax12), (ax13, ax14)) = plt.subplots(nrows=2, ncols=2, figsize = (6,4) )#, layout='constrained'
ax11.contourf(ImPro[:,:,0], cmap = "hot")
ax11.scatter(COMTotal[1,0], COMTotal[0,0], c = "b")
ax11.set_title("Time = " + plot1Time + "s" + plot1frames)
ax12.contourf(ImPro[:,:,1], cmap = "hot")
ax12.scatter(COMTotal[1,1], COMTotal[0,1], c = "b")
ax12.set_title("Time = " + plot2Time + "s" + plot2frames)
ax13.contourf(ImPro[:,:,2], cmap = "hot")
ax13.scatter(COMTotal[1,2], COMTotal[0,2], c = "b")
ax13.set_title("Time = " + plot3Time + "s" + plot3frames)
ax14.contourf(ImPro[:,:,3], cmap = "hot")
ax14.scatter(COMTotal[1,3], COMTotal[0,3], c = "b")
ax14.set_title("Time = " + plot4Time + "s" + plot4frames)
plt.show()