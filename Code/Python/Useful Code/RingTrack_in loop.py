import matplotlib.pyplot as plt
import numpy as np

import os
import sys

dirPath = os.getcwd()
sys.path.insert(0, dirPath)
import OllieTools as oj


import cv2
import glob
from scipy import ndimage
import concurrent.futures
from scipy.fft import fft2,fftshift, ifft2

i = 0
startFrames = [60, 37, 72, 67, 70, 82, 72, 72, 72, 68]
endFrames = [350, 350, 414, 297, 341, 264, 283, 354, 376, 430]
tmpstartFrames = 0
tmpendFrames = 0

def Load():
    global Dir, FileList, col, Circle, Im0filt, COMTotal, number, t, frame_slicer3001
    frame_slicer3001 = 50
    fps = 25
    Dir = 'E:\Repeatibility/3RPM\Ring{}_3RPM\Side/*'.format(i+1) #########################################
    skip = 10
    FileList = sorted(glob.glob(Dir)) [tmpstartFrames:tmpendFrames:skip] #specific frames desired (start:stop:step)  #######################################
    t = np.arange(len(FileList))*skip/fps
    col = 1     #colour to be filtered for Red = 0, Green = 1, Blue = 2
    Im0 = cv2.imread(FileList[0])
    Im0 = Im0[:,frame_slicer3001:]
    Circle = oj.draw_cicle((Im0.shape[0], Im0.shape[1]), 100)
    Im0Cv = cv2.cvtColor(Im0, cv2.COLOR_BGR2RGB)
    Im0filt = oj.LowPass2D(Im0Cv[:,:,col], Circle)
    COMTotal = np.zeros((2, len(FileList)))
    number = list(range(1, len(FileList)))
    # mean = 50*np.mean(Im0filt)
    print('LOADED')

def Track(ImN):
    ImTmp = cv2.imread(FileList[ImN])
    ImTmp = ImTmp[:,frame_slicer3001:]
    ImTmpCv = cv2.cvtColor(ImTmp, cv2.COLOR_BGR2RGB)
    ImTmpfilt = oj.LowPass2D(ImTmpCv[:,:,col], Circle)
    ImTmpTest = np.abs(ImTmpfilt - Im0filt)
    mean = 20*np.mean(ImTmpTest)
    ImTmpTest[ImTmpTest < mean] = 0 
    if np.any(ImTmpTest > 0)  == True:
        COMTotal[:,ImN] = ndimage.measurements.center_of_mass(ImTmpTest)
    else:
        COMTotal[:,ImN] = 0

def PostPro():
    # np.savez('E:\Repeatibility\Ring Tracking Data\Variables/3RPM', Ring1_3 = COMTotal)
    # oj.AppendSave("Ring{}_3".format(i+1), COMTotal, "E:\Repeatibility\Ring Tracking Data\Variables/3RPM.npz") ##################################
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot()
    ax.plot(t[1:], COMTotal[1,1:])
    plt.ylim(0)
    ax.set_title("3 RPM Path")
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Distance [pixels]')
    plt.show()
    # fig.savefig("E:\Repeatibility\Ring Tracking Data/3RPM/Ring{}_3.png".format(i+1))

for i in range(1):
# for i in range(1,10):
    tmpstartFrames = startFrames[i]
    tmpendFrames = endFrames[i]
    print("i = " + str(i))
    print("i+1 =" + str(i+1))    
    print(tmpstartFrames)
    print(tmpendFrames)
    if __name__ == "__main__":
        Load()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(Track, number)
        PostPro()