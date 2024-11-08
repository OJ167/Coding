import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

import os
import sys

import h5py
import cv2
import glob
from scipy import ndimage, io
from scipy.ndimage.filters import gaussian_filter
from scipy import interpolate
import concurrent.futures
from scipy.fft import fft2,fftshift, ifft2, fft, fftfreq, ifft, rfft, rfftfreq
import mat73
import pathlib
from scipy.interpolate import interp1d, RectBivariateSpline
import time
import math
import itertools

#####Import Ollie Tools
dirPath = "C:/Coding/Code"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)

plt.style.use(["science", "vibrant", "no-latex"])
cmap = plt.get_cmap("jet_r")


def animate_cube_contourf(
    cube_array, interval=16.7, cmap="bwr", save=0, output="15.mp4", fps=90, scale = 1, fsize = (12, 10)
):

    """
    animates a numpy 3D Array for quick visualisation (specific to contourf).

    INPUT:
        cube_array  : name of 3D numpy array that needs to be animated.
        interval    : #of ms between each frame.
        cmap        : colormap. Default='bwr'

    OUTPUT:
        animated window going through the cube.

    """

    fig, ax = plt.subplots(figsize=fsize)
    vmin = -np.max(np.abs(cube_array))
    vmax = np.max(np.abs(cube_array))
    def animate(i):
        ax.clear()
        ax.contourf(cube_array[i, :, :], cmap=cmap, levels = np.linspace(scale*vmin,scale*vmax,20))
        ax.set_title("%03d" % (i))

    ani = animation.FuncAnimation(
        fig, animate, frames=cube_array.shape[0], interval=interval, blit=False
    )

    # plt.colorbar()
    if save == 0:
        plt.show()
    # else:
    # ani.save(output, writer="ffmpeg", fps=fps, dpi=160)


def AppendSave(str, array, file):
    """
    Appends a new variable (only one) to an existing .npz file. If one does not exist use np.savez(os.path.join(directory, OutputStr), varaible = variable)

    INPUT:
        str             : Name for appended data variable
        array           : Data to be appended to existing file,
        file            : String for filename and location of file to adjust.

    """

    data = np.load(file)
    data = dict(data)
    data[str] = array
    np.savez(file, **data)
    print(f"Data saved - {file}")


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


def FlipArrayVert(u, v):
    """
    Rotates velocity fields for u and v
    INPUT:
        u           : 3D Numpy tensor containing velocity data
        v           : 3D Numpy tensor containing velocity data

    OUTPUT:
        u           : 3D Numpy tensor containing velocity data, flipped vertically.
        v           : 3D Numpy tensor containing velocity data, flipped vertically.

    """
    u = np.flip(u, axis=1)
    v = -np.flip(v, axis=1)
    return u, v


def velocityTracking(u, v):
    """
    finding the location of the ring using velocity
    """
    uMax = np.zeros(u.shape[0])
    uMin = np.zeros(u.shape[0])
    for t in range(0, u.shape[0]):
        uMax[t] = np.argmax(u[t,int(u.shape[1]/2),:])
        uMin[t] = np.argmin(u[t,int(u.shape[1]/2),:])
    # f2, ax2 = plt.subplots(nrows=1, ncols=1)
    # ax2.plot(uMax)
    # ax2.plot(uMin)
    # plt.show()
    return uMax, uMin


def velocityPeakTracking(vort, l = 0):
    VortLocMax = np.zeros((vort.shape[0], 2))
    VortLocMin = np.zeros((vort.shape[0], 2))
    if l == 0:
        l = vort.shape[0]
    elif l > vort.shape[0]:
        l = vort.shape[0]
    for i in range(l):
    # for i in range(500,vort.shape[0]):
        color = cmap(float(i) / l)
        vortTemp = vort[i, :, :]
        VortLocMax[i,:] = np.argwhere(vortTemp == np.max(vortTemp))
        VortLocMin[i,:] = np.argwhere(vortTemp == np.min(vortTemp))
        plt.scatter(VortLocMax[i,1], VortLocMax[i,0], color = color)
        plt.scatter(VortLocMin[i,1], VortLocMin[i,0], color = color)        
    plt.show()


def importData73(dir):
    """
    loads matlab data from a .MAT file. Crucially the variables loaded in the file are 'u_filtered' and v_filtered.

    INPUT:
        dir         : Full path of file to be opened, must include file extension.

    OUTPUT:
        u           : 3D Numpy tensor containing velocity data, has not been scaled.
        v           : 3D Numpy tensor containing velocity data, has not been scaled.
    """

    os.chdir(os.path.dirname(dir))
    mat_contents = mat73.loadmat(os.path.basename(dir))
    u_temp = np.squeeze(mat_contents["u_filtered"])
    v_temp = np.squeeze(mat_contents["v_filtered"])
    u = np.empty((u_temp.shape[0], u_temp[0].shape[0], u_temp[0].shape[1]))
    for i in range(u.shape[0]):
        u[i] = u_temp[i]
    v = np.empty((v_temp.shape[0], v_temp[0].shape[0], v_temp[0].shape[1]))
    for i in range(v.shape[0]):
        v[i] = v_temp[i]
    print(str("Filtered Data Imported  -  " + str(u.shape)))
    u, v = FlipArrayVert(u, v)
    return u, v


def importData(dir):
    """
    loads matlab data from a .MAT file. Crucially the variables loaded in the file are 'u_filtered', 'v_filtered', and 'vorticity'.

    INPUT:
        dir         : Full path of file to be opened, must include file extension.

    OUTPUT:
        u           : 3D Numpy tensor containing velocity data, has not been scaled.
        v           : 3D Numpy tensor containing velocity data, has not been scaled.
        vort        : 3D Numpy tensor containing vorticity data, has not been scaled.
    """

    os.chdir(os.path.dirname(dir))
    mat_contents = io.loadmat(os.path.basename(dir))
    u_temp = np.squeeze(mat_contents["u_filtered"])
    print(u_temp.shape)
    v_temp = np.squeeze(mat_contents["v_filtered"])
    # vort_temp = np.squeeze(mat_contents["vorticity"])
    u = np.empty((u_temp.shape[0], u_temp[0].shape[0], u_temp[0].shape[1]))
    print(u_temp[0].shape[0])
    for i in range(u.shape[0]):
    # for i in range(1499):
        u[i] = u_temp[i]
    v = np.empty((v_temp.shape[0], v_temp[0].shape[0], v_temp[0].shape[1]))
    for i in range(v.shape[0]):
    # for i in range(1499):
        v[i] = v_temp[i]
    print(str("Filtered Data Imported  -  " + str(u.shape)))
    u, v = FlipArrayVert(u, v)

    # vorticity = np.empty((vort_temp.shape[0], vort_temp[0].shape[0], vort_temp[0].shape[1]))
    # for i in range(vorticity.shape[0]):
    #     vorticity[i] = vort_temp[i]

    return u, v, #vorticity


def importVorticity(dir):
    """
    loads matlab data from a .MAT file. Crucially the variables loaded in the file are 'u_filtered', 'v_filtered', and 'vorticity'.

    INPUT:
        dir         : Full path of file to be opened, must include file extension.

    OUTPUT:
        vort        : 3D Numpy tensor containing vorticity data, has not been scaled.
    """

    os.chdir(os.path.dirname(dir))
    mat_contents = io.loadmat(os.path.basename(dir))
    vort_temp = np.squeeze(mat_contents["vorticity"])
    vorticity = np.empty((vort_temp.shape[0], vort_temp[0].shape[0], vort_temp[0].shape[1]))
    for i in range(vorticity.shape[0]):
        vorticity[i] = vort_temp[i]
    print(str("Filtered Data Imported  -  " + str(vorticity.shape)))

    return vorticity


def scaleVel(u, v, fps, heightPixels=1976, heightImage=0.405):
    """
    Scales velocity fields for u and v based on image height, n pixels and the fps of the camera.

    INPUT:
        u           : 3D Numpy tensor containing velocity data, has not been scaled.
        v           : 3D Numpy tensor containing velocity data, has not been scaled.

    OUTPUT:
        u           : 3D Numpy tensor containing scaled velocity data.
        v           : 3D Numpy tensor containing scaled velocity data.
    """

    factor = fps * heightImage / heightPixels
    u = factor * u
    v = factor * v
    return u, v

def scaleVelNozzle(u, v, fps, heightPixels=1976, heightImage=0.405):
    """
    Scales velocity fields for u and v based on image height, n pixels and the fps of the camera.

    INPUT:
        u           : 3D Numpy tensor containing velocity data, has not been scaled.
        v           : 3D Numpy tensor containing velocity data, has not been scaled.

    OUTPUT:
        u           : 3D Numpy tensor containing scaled velocity data.
        v           : 3D Numpy tensor containing scaled velocity data.
    """

    factor = fps * heightImage / heightPixels
    u = factor * u
    v = factor * v
    return u, v


def calculate_vorticity(u, v):
    """
    calculates vorticity of velocity field
     
    INPUT:
        u           : 3D Numpy tensor containing velocity data
        v           : 3D Numpy tensor containing velocity data

    OUTPUT:
        Vorticity   : 3D Numpy tensor containing velocity data
        vorticity_gauss : 3D Numpy tensor containing velocity data after a gausian filter

    """
    dv = np.gradient(v, axis = 2)
    du = np.gradient(u, axis = 1)
    vorticity = dv - du
    vorticity_gauss = gaussian_filter(vorticity, sigma = 0.7)
    return vorticity, vorticity_gauss


def vorticity_animation(u, v): 
    """
    calculates vorticity of velocity field

    INPUT:
        u           : 3D Numpy tensor containing velocity data
        v           : 3D Numpy tensor containing velocity data

    OUTPUT:
        Vorticity   : 3D Numpy tensor containing velocity data
        vorticity_gauss : 3D Numpy tensor containing velocity data after a gausian filter

    """
    dv = np.gradient(v, axis = 2)
    du = np.gradient(u, axis = 1)
    
    vorticity = dv - du
    vorticity_gauss = gaussian_filter(vorticity, sigma = 0.7)

    fig3, (ax3 , ax4)= plt.subplots(nrows=2, ncols=1)
    ax3.contourf(vorticity[100,:,:])
    ax4.contourf(vorticity_gauss[100,:,:])
    plt.show()

    plt.figure()
    plt.ion()
    for i in range(vorticity.shape[0]):
        print(i)
        plt.contourf(vorticity_gauss[i,:,:])
        plt.pause(0.01)


def vorticityPeakTracking(u, v, l = 0):
    """
     Finds the center of a vortex in a 2D velocity field using the local maximum enstrophy field.
    It does this for each time step in a field of length u.shape[0]

    Args:
        u: The x-component of the velocity field.
        v: The y-component of the velocity field.

    Returns:
        The center of the vortex, as an array of (y, x) coordinates.   
    """
    vorticity, vort_gauss = calculate_vorticity(u, v)
    VortLocMax = np.zeros((vort_gauss.shape[0], 2)) #same length in time as vorticity field, 2 rows - 0 for y, 1 for x
    VortLocMin = np.zeros((vort_gauss.shape[0], 2)) #same length in time as vorticity field, 2 rows - 0 for y, 1 for x

    if l == 0:
        l = vort_gauss.shape[0]
    elif l > vort_gauss.shape[0]:
        l = vort_gauss.shape[0]
    
    for i in range(l):
        vortTemp = vort_gauss[i, :, :]
        VortLocMax[i,:] = np.argwhere(vortTemp == np.max(vortTemp))
        VortLocMin[i,:] = np.argwhere(vortTemp == np.min(vortTemp))

    return VortLocMax, VortLocMin


    #calculating tilt

    # delta_y = np.zeros((gauss.shape[0], 2))
    # delta_x = np.zeros((gauss.shape[0], 2))

    # delta_y = VortLocMax[:, 0] - VortLocMin[:, 0]
    # delta_x = VortLocMax[:, 1] - VortLocMin[:, 1]

    # # print(delta_y)
    # # print(delta_x)

    # tilt = np.arctan(abs(delta_y / delta_x))
    # print(tilt)
    # f1, (ax2) = plt.subplots(nrows=1, ncols=1)
    # ax2.plot(tilt)
    # plt.show()


def vorticityPeakTracking_i(u, v, l = 0, n = 0):
    vorticity, vort_gauss = calculate_vorticity(u, v)
    VortLocMax_i = np.zeros((n, vort_gauss.shape[0], 2)) #same length in time as vorticity field, 2 rows - 0 for y, 1 for x
    VortLocMin_i = np.zeros((n, vort_gauss.shape[0], 2)) #same length in time as vorticity field, 2 rows - 0 for y, 1 for x
    Core_gradient = np.zeros((vort_gauss.shape[0], 2)) # not working yet

    if l == 0:
        l = vort_gauss.shape[0]
    elif l > vort_gauss.shape[0]:
        l = vort_gauss.shape[0]
    
    for j in range(n):
        for i in range(l):
        # for i in range(150, 1200):
            vortTemp = vort_gauss[i, :, :]
            VortLocMax_i[ i,:] = np.argwhere(vortTemp == np.max(vortTemp))
            VortLocMin_i[j, i,:] = np.argwhere(vortTemp == np.min(vortTemp))

    # f1, (ax1) = plt.subplots(nrows=1, ncols=1)
    # ax1.scatter(VortLocMax[:, 1], VortLocMax[:, 0])
    # ax1.scatter(VortLocMin[:, 1], VortLocMin[:, 0])

    # # Ploting a midline
    # midline = np.zeros(vort_gauss.shape[0])
    # midline[:] = vort_gauss.shape[1]/2
    # ax1.plot(midline[0:vort_gauss.shape[2]])
    # plt.show()

    return VortLocMax_i, VortLocMin_i


def PlotVelocity(u, v, frame):
    V = u + v
    print(V.shape)
    f1, ax1 = plt.subplots(nrows=1, ncols=1)
    ax1.contourf(V[frame,:,:])
    plt.show()   


def IWFilter(inputArray, input_ang, fps, rpm, forcedFreq = 0):
    """
    FFT filter for inertial wave frequency.
    
    Parameters
    ----------
    inputArray : array
        3D Array to be filtered.

    input_ang : int

    fps : int

    rpm : int

    Returns
    -------
    v_postFFT : array
        3D output array of filtered data.  

    """
    v_fluc = inputArray.copy()
    v1 = np.mean(v_fluc, axis=0)
    v_fluc -= v1
    if forcedFreq == 0:
        filtfreq = FiltFreqCalc(input_ang,fps=fps,rpm=rpm)
    else:
        filtfreq = forcedFreq
    
    print(f'Filter Frequency = {np.round(filtfreq, 4)}Hz')

    thresh = 0.03
    # thresh = 0.09
    # thresh = 0.1

    v_FFT = fft(v_fluc, axis=0)
    FFTFreq = fftfreq(v_fluc.shape[0], 1 / fps)
    
    mask1 = np.where(np.logical_and(filtfreq-thresh<FFTFreq, filtfreq+thresh>FFTFreq))
    mask2 = np.where(np.logical_and(-filtfreq-thresh<FFTFreq, -filtfreq+thresh>FFTFreq))
    
    window1 = np.zeros_like(FFTFreq)
    window1[mask1] = 1
    width = np.sum(window1)
    window1[mask1] = np.hanning(width)
    
    window2 = np.zeros_like(FFTFreq)
    window2[mask2] = 1
    window2[mask2] = np.hanning(width)

    windowT = window1 + window2

    v_FFT = v_FFT*windowT[:, None, None]

    v = ifft(v_FFT, axis=0)
    v_postFFT = np.real(v)

    return v_postFFT


def FiltFreqCalc(angle, fps, rpm):
    """
    Calculates the Inertial wave oscillation frequency using given parameters. 
    
    Parameters
    ----------
    angle : int

    fps : int

    rpm : int

    Returns
    -------
    filt_freq : float
        Frequency in Hz. 

    """
    f_omega = (rpm/60)
    ang = np.cos(np.deg2rad(angle))
    filt_freq = 2*f_omega*ang

    return filt_freq


def quivPlot(u, v):
    quiv, ax = plt.subplots(constrained_layout=True)
    uM = u
    vM = v
    mag = np.sqrt(uM**2 + vM**2)
    vmax = np.amax(vM)
    ax.contourf(mag)
    quiver = ax.quiver(uM, vM, pivot="middle")
    quiv.colorbar(
        plt.cm.ScalarMappable(),
        shrink=0.8,
        label="Axial Velocity (m/s)",
    )
    # cbar.set_label('Velocity (m/s)')
    # quiv.title('Contour / Quiver showing u, v')
    ax.set_xlabel("x Location")
    ax.set_ylabel("y Location")
    plt.show()


def progressBar(step,nSteps, width=40):

    percent = int(np.ceil(step*100/nSteps))

    left = width * percent // 100
    right = width - left
    
    tags = "#" * left
    spaces = " " * right
    percents = f"{percent:.0f}%"
    
    print("\r[", tags, spaces, "]", percents, sep="", end="", flush=True)


def NDUnitsForPlotsWide(shapeX, shapeY, widthM = 0.66, HeightM = 1.066, jetLocPix = 600, pixX = 1200, d = 0.05):
    """
    shapeX becomes Radial
    shapeY becomes Z
    """
    shapeX = shapeX -1
    zeroPos = int(jetLocPix/pixX * shapeX)

    r = np.linspace(-widthM * zeroPos/shapeX, widthM * (shapeX-zeroPos)/shapeX, shapeX+1)
    r_nd = r / d

    z = np.linspace(0, HeightM, shapeY)
    z_nd = z / d

    return r_nd, z_nd


def NDUnitsForPlotsNozzle(shapeX, shapeY, widthM = 0.13574, HeightM = 0.21719, jetLocPix = 600, pixX = 1200, d = 0.05):
    """
    shapeX becomes Radial
    shapeY becomes Z
    """
    shapeX = shapeX -1
    zeroPos = int(jetLocPix/pixX * shapeX)

    r = np.linspace(-widthM * zeroPos/shapeX, widthM * (shapeX-zeroPos)/shapeX, shapeX+1)
    r_nd = r / d*2

    z = np.linspace(0, HeightM, shapeY)
    z_nd = z / d*2
    # z_nd = z_nd - 0.55
    z_nd = z_nd - 1.1
    
    return r_nd, z_nd


def InterpZeros(y):
    if (y==0).any() == True:
        y = np.array(y)
        x = np.arange(y.shape[0])
        idx = np.nonzero(y)
        f = interpolate.interp1d(x[idx], y[idx], fill_value="extrapolate" )
        ynew = f(x)
    else:
        ynew = y
    return ynew


def FilterSpikes(inputArray, deviation = 50):
    diffArray = np.diff(inputArray)
    inputArray[1:] = np.where(diffArray>deviation,0,inputArray[1:])
    inputArray = InterpZeros(inputArray)
    return inputArray


def animate_cube_contourf_points(
    cube_array, VortLocMax, VortLocMin, interval=17, cmap="seismic", save=0, output="points2.mp4", fps=60, scale = 1, fsize = (10, 8), 
):

    """
    animates a numpy 3D Array for quick visualisation (specific to contourf). This function animates the vorticity field with points indicating 
    max and min vorticity.

    INPUT:
        cube_array  : name of 3D numpy array that needs to be animated.
        interval    : #of ms between each frame.
        cmap        : colormap. Default='bwr'

    OUTPUT:
        animated window going through the cube.

    """
    print("Start")
    fig, ax1 = plt.subplots(nrows = 1, ncols = 1, figsize=fsize, sharex = True, sharey = True)
    vmin = -np.max(np.abs(cube_array))
    vmax = np.max(np.abs(cube_array))
    def animate(i):
        ax1.clear()
        ax1.contourf(cube_array[i, :, :], cmap=cmap, levels = np.linspace(scale*vmin,scale*vmax,20))
        ax1.scatter(VortLocMax[i,1],VortLocMax[i,0], label = "Max Vorticity", color = "k")
        ax1.scatter(VortLocMin[i,1],VortLocMin[i,0], label = "Min Vorticity", color = "w")
        x1, x2 = VortLocMax[i,1], VortLocMin[i,1]
        y1, y2 = VortLocMax[i,0], VortLocMin[i,0]
        ax1.plot([x1,x2],[y1,y2], "g--", linewidth=2.0)
        ax1.set_title("%03d" % (i))
    print("2")
    anim = animation.FuncAnimation(
        fig, animate, frames=cube_array.shape[0], interval=interval, blit=False
    )

    if save == 0:
        plt.show()
    else:
        print("save loop")
        anim.save(output, writer="ffmpeg", fps=fps, dpi=160)

    # writervideo = animation.FFMpegWriter(fps=60)
    # anim.save(output, writer=writervideo, dpi=160)

    # anim.save(output, writer="ffmpeg", fps=fps, dpi=160)


# def load():
#     global dirRoot, mtx, dist, short, FileListTop, FileListBot, number, n 
#     Port = 'F'
#     short = 1
#     dirRoot = "F:/1.Experiments/RPM-30__Pump-10/2022-09-08__FPS-30/1"

#     mtx, dist = oj.load_coefficients(f'{Port}:/1. Calibration files/07-03-23/calibration_chessboard.yml')
#     # mtxB, distB = sb.load_coefficients(f'{Port}:/.EXPERIMENTS/Calibration Files/22-09-01/CalB/calibration_chessboard.yml')
#     # mtxT, distT = sb.load_coefficients('F:/2.Calibration Files/22-05-12/calibration_chessboard.yml')

#     dirTop = str(dirRoot + "/T/*")
#     dirBot = str(dirRoot + "/B/*")
#     chars = len(os.listdir(str(dirTop)[:-1])[0])

#     if chars > 12:
#         oj.renameFiles(str(dirTop)[:-1])
#         oj.renameFiles(str(dirBot)[:-1])
#         print("Files Renamed")
#     else:
#         pass

#     FileListTop = sorted(glob.glob(dirTop))
#     FileListBot = sorted(glob.glob(dirBot))
#     # Define cropping size
#     n = 55

#     number = list(range(0, len(FileListBot) - 2))


# def process_image(number):
#     top = cv2.imread(FileListTop[number])
#     dstTop = cv2.undistort(top, mtx, dist, None, None)[:-n, :]
#     bottom = cv2.imread(FileListBot[number+2])
#     dstBottom = cv2.undistort(bottom, mtx, dist, None, None)[n:, :] 
#     merged = cv2.vconcat([dstTop, dstBottom]) #[top,bottom])
#     numPad = str(number)
#     numPad = numPad.zfill(5)
#     cv2.imwrite(str(dirRoot + f"/M/Image_{numPad}.tiff"), merged)
#     if short == 1:
#         if number % 60 == 0:
#             cv2.imwrite(str(dirRoot + f'/Short/{str(int(numPad/60))}.tiff'), merged)
#         else:
#             pass
#     else:
#         pass
#     print(f"done     file: {number}")


# if __name__ == "__main__":
#     load()
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         executor.map(process_image, number)


def renameFiles(dir):
    """
    loads .tiff images from a directory and changes their name to '00001.tiff' The number is detected by looking for a dash in the filename

    INPUT:
        dir         : Directory of files to open, must end in *. e.g. \Images\*

    """
    listFiles = sorted(os.listdir(dir))
    length = len(listFiles)

    for i in range(0, length):  # length
        fileOld = os.path.join(dir, listFiles[i])
        Position = int(str(listFiles[i]).rfind("-")) + 1
        Number = str(listFiles[i])[Position:-5]
        NumPad = Number.zfill(5)
        FnNew = str(NumPad + ".tiff")
        fileNew = os.path.join(dir, FnNew)
        os.rename(fileOld, fileNew)


def calibrate_chessboard2(dir_path, image_format, square_size, width, height):
    """

    Calibrate a camera using chessboard images.

    INPUT:
        dir_path:       path to the directory where the chessboard images are stored.
        image_format:   extension of the images to be used.
        square_size:    size, in centimeter, of each square of the real chessboard. Use a ruler and try to be as accurate as possible.
        width, height:  how many squares there are in the chessboard (in my case, 6 x 9.
    OUTPUT:
        [ret, mtx, dist, rvecs, tvecs]

    """
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,6,0)
    objp = np.zeros((height * width, 3), np.float32)
    objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)

    objp = objp * square_size

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    images = pathlib.Path(dir_path).glob(f"*.{image_format}")
    # Iterate through all images
    for fname in images:
        img = cv2.imread(str(fname))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (width, height), None)

        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            img = cv2.drawChessboardCorners(img, (width, height), corners2, ret)
            cv2.imshow("img", img)
            cv2.waitKey(1000)

    # Calibrate camera
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )

    return [ret, mtx, dist, rvecs, tvecs]

def save_coefficients(mtx, dist, path):
    """Save the camera matrix and the distortion coefficients to given path/file."""
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_WRITE)
    cv_file.write("K", mtx)
    cv_file.write("D", dist)
    # note you *release* you don't close() a FileStorage object
    cv_file.release()


def load_coefficients(path):
    """Loads camera matrix and distortion coefficients."""
    # FILE_STORAGE_READ
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)

    # note we also have to specify the type to retrieve other wise we only get a
    # FileNode object back instead of a matrix
    camera_matrix = cv_file.getNode("K").mat()
    dist_matrix = cv_file.getNode("D").mat()

    cv_file.release()
    return [camera_matrix, dist_matrix]


def sum_kinetic_energy(u, v):
    V = np.sqrt((abs(u))**2 + (abs(v))**2)
    kinetic_energy = np.square(V)
    sum_kinetic_energy = np.sum(kinetic_energy, axis=(1,2))
    # print(sum_kinetic_energy.shape)
    return kinetic_energy, sum_kinetic_energy


def frames_to_seconds(u, v, FPS):
    """for plotting in seconds"""
    data_length = u.shape[0]   # 10 seconds of data at 60Hz
    sample_rate =  FPS

    # calculate the time step
    time_step = 1/sample_rate

    # create the time series
    time = np.arange(0, data_length*time_step, time_step)
    return time


def animate_cube_quiver( 
    u, v, u_az, interval=11.1, cmap="bwr", save=0, output="15.mp4", Dir="C:/Users/u2088308/Videos", name="vid.mp4", fps=90, scale = 1, fsize = (19, 12)
):

    """
    animates a numpy 3D Array for quick visualisation (specific to quiver plot).

    INPUT:
        cube_array  : name of 3D numpy array that needs to be animated.
        interval    : no. of ms between each frame.
        cmap        : colormap. Default='bwr'

    OUTPUT:
        animated window going through the cube.

    """

    # x, y = np.meshgrid(np.arange(0, 111, 1), np.arange(0, 69, 1))
    x, y = np.meshgrid(np.arange(0, 111, 1), np.arange(0, 69, 1))
    V = np.sqrt((abs(u**2) + abs(v**2)))
    # r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
    time = oj.frames_to_seconds(u, v, fps)

    output = str(Dir) + str(name)
    print(output)

    fig, ax = plt.subplots(figsize=fsize)
    vmin = -np.max(np.abs(V))
    vmax = np.max(np.abs(V))
    def animate(i):
        ax.clear()
        ax.contourf(u_az[i, :, :], cmap=cmap, levels = np.linspace(scale*vmin,scale*vmax,20))
        # ax.quiver(z_nd, r_nd, u[i,:,:], v[i,:,:], pivot="middle")
        ax.quiver(u[i,:,:], v[i,:,:], pivot="middle")
        ax.set_title("Time " + str("%.1f") %time[i])
        ax.set_title("%0.2d" % i)
        # ax.set_xlabel("z/D")
        # ax.set_ylabel("r/D")

    ani = animation.FuncAnimation(
        fig, animate, frames=V.shape[0], interval=interval, blit=False
    )

    # plt.colorbar()
    if save == 0:
        plt.show()  
    else:
        ani.save(output, writer="ffmpeg", fps=fps, dpi=80)
    # ani.save("output.gif")
    # writervideo = animation.FFMpegWriter(fps=fps)
    # FFwriter = animation.FFMpegWriter()
    # ani.save(output, dpi=80, writer = FFwriter)


def sum_Vorticity(
    u, v, l = 0
):
    vorticity, vorticity_gauss = calculate_vorticity(u, v)
    sumVorticity = np.zeros((u.shape[0]))


    if l == 0:
        l = vorticity.shape[0]
    elif l > vorticity.shape[0]:
        l = vorticity.shape[0]

    for i in range(l):
        vortTemp = vorticity[i, :, :]
        sumVorticity[i] = np.sum(abs(vorticity[i, :, :]))
    return sumVorticity


def sum_Enstrophy(
    u, v, l = 0        
):
    vorticity, vorticity_gauss = calculate_vorticity(u, v)
    sumEnstrophy = np.zeros((u.shape[0]))


    if l == 0:
        l = vorticity.shape[0]
    elif l > vorticity.shape[0]:
        l = vorticity.shape[0]

    for i in range(l):
        vortTemp = vorticity[i, :, :]
        sumEnstrophy[i] = np.sum((vorticity[i, :, :]**2))
    return sumEnstrophy


def create_Mean(
        n, Dir
):
    ######## Importing multiple rings #####
    # n = 10
    u, v = oj.importData73(str(Dir) + "1/Data/PIV_export_fine.mat")
    print(str(Dir), "\r")
    u = np.zeros([n, u.shape[0], u.shape[1], u.shape[2]])
    v = np.zeros([n, v.shape[0], v.shape[1], v.shape[2]])

    for i in range(1, n+1):
        u[(i-1),:,:,:], v[(i-1),:,:,:] = oj.importData73(str(Dir) + str(i) + "/Data/PIV_export_fine.mat")
        oj.progressBar(i, n)

    u_mean = np.mean(u[1:], 0)
    v_mean = np.mean(v[1:], 0)
    # u_mean, v_mean = gaussian_filter(u_mean, sigma=0.7), gaussian_filter(v_mean, sigma=0.7)

    return u_mean, v_mean


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



def animate_Line( 
    u, row = 13, interval=11.1, save=0, output="15.mp4", fps=90, scale = 1, fsize = (19, 12)
):

    """
    animates a Line from a 3D Array for quick visualisation.

    INPUT:
        cube_array  : name of 3D numpy array that needs to be animated.
        interval    : no. of ms between each frame.


    OUTPUT:
        animated line graph.

    """

    r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
    time = oj.frames_to_seconds(u, u, fps)

    fig, ax = plt.subplots(figsize=fsize)

    def animate(i):
        ax.clear()
        ax.plot(r_nd, u[i,:, row])
        ax.set_title("Time " + str("%.1f") %time[i])
        ax.set_xlabel("r/D")
        ax.set_ylabel("u")
        ax.set_ylim(np.min(u), np.max(u))

    ani = animation.FuncAnimation(
        fig, animate, frames=u.shape[0], interval=interval, blit=False
    )

    # plt.colorbar()
    if save == 0:
        plt.show()  
    else:
        ani.save(output, writer="ffmpeg", fps=fps, dpi=80)


def ConvertCylindrical(xArg, yArg, X, Y, u, v):

    widthM = np.max(X)
    heightM = np.max(Y)
    x0 = (xArg * widthM / X.shape[0])
    y0 = (yArg * heightM / Y.shape[0])
    X = X - x0
    Y = Y - y0

    X, Y = np.meshgrid(X,Y)

    r = np.sqrt(X**2 + Y**2)
    theta = np.arctan2(Y, X)

    U_r = u * np.cos(theta) + v * np.sin(theta)

    U_az = v * np.cos(theta) - u * np.sin(theta)

    return r, theta, U_r, U_az, x0, y0

def binCylindrical(r, theta, U_r, U_az, thetaBins = 18, rBins = 36):

    U_rBins = np.zeros((rBins, thetaBins))
    U_azBins = np.zeros((rBins, thetaBins))
    theta_arr = (np.pi * 2) * (np.arange(thetaBins)+0.5) / thetaBins
    r_arr = np.max(r) * (np.arange(rBins)+0.5) / rBins
    # print(U_rBins.shape)
    # print(U_rBins)
    for thetaVal in range(thetaBins-1):
        # print(thetaVal)
        for rVal in range(rBins-1):
            # print(rVal)
            mask = np.where((theta > (-np.pi + (2 * np.pi) * thetaVal / thetaBins)) | (theta < -np.pi + (2 * np.pi) * (thetaVal + 1) / thetaBins) | (r > np.max(r) * rVal / rBins) | (r < np.max(r) * (rVal + 1) / rBins))
            # print(U_r[mask])
            U_rBins[rVal, thetaVal] = np.mean(U_r[mask])
            # print(np.mean(U_r[mask]))
            U_azBins[rVal, thetaVal] = np.mean(U_az[mask])
    # print(U_rBins)
    return r_arr, theta_arr, U_rBins, U_azBins



def find_vortex_center_Vorticity(u, v, guass = 3, range = 3):
    """
    Finds the center of a vortex in a 2D velocity field using the vorticity field and interpolating the maxima location using a 2nd order bilinear polynomial fit at a resolution of 100* the original.

    Args:
        u: The x-component of the velocity field.
        v: The y-component of the velocity field.

    Returns:
        The center of the vortex, as a tuple of (x, y) coordinates.
    """
    scale = 0.05
    dvdx = np.gradient(v, axis=1)
    dudy = np.gradient(u, axis=0)
    
    vorticity = (dvdx - dudy)
    vortSmooth = np.abs(ndimage.gaussian_filter(vorticity, guass))

    MaxLoc = np.argwhere(vortSmooth == np.max(vortSmooth))[0]
    if MaxLoc[0] < 15 or MaxLoc[0] > u.shape[0] - 15 or MaxLoc[1] < 15 or MaxLoc[1] > u.shape[1] - 15:
        xNew, yNew = 0, 0
    else:
        Sect = vortSmooth[MaxLoc[0]-range:MaxLoc[0]+range+1, MaxLoc[1]-range:MaxLoc[1]+range+1]
        # ax2.contourf(Sect)
        SplineSect = RectBivariateSpline(np.arange(Sect.shape[-2]), np.arange(Sect.shape[-1]), Sect, kx = 2, ky = 2)
        SectDetailed = SplineSect(np.arange(0, Sect.shape[-2]-1, scale), np.arange(0, Sect.shape[-1]-1, scale), grid=True)
        # ax3.contourf(SectDetailed)
        yNew = MaxLoc[0]-range + np.argwhere(SectDetailed == np.max(SectDetailed))[0][0] * scale
        xNew = MaxLoc[1]-range + np.argwhere(SectDetailed == np.max(SectDetailed))[0][1] * scale

    return xNew, yNew, vorticity, vortSmooth

def find_vortex_Max_center(vorticity, guass = 3, range = 3):
    """
    Finds the center of a vortex in a 2D velocity field using the vorticity field and interpolating the maxima location using a 2nd order bilinear polynomial fit at a resolution of 100* the original.

    Args:
        u: The x-component of the velocity field.
        v: The y-component of the velocity field.

    Returns:
        The center of the vortex, as a tuple of (x, y) coordinates.
    """
    scale = 0.05

    vortSmooth = ndimage.gaussian_filter(vorticity, guass)

    MaxLoc = np.argwhere(vortSmooth == np.max(vortSmooth))[0]
    if MaxLoc[0] < 5 or MaxLoc[0] > vorticity.shape[0] - 5 or MaxLoc[1] < 5 or MaxLoc[1] > vorticity.shape[1] - 5:
        xNew, yNew = 0, 0
    else:
        Sect = vortSmooth[MaxLoc[0]-range:MaxLoc[0]+range+1, MaxLoc[1]-range:MaxLoc[1]+range+1]
        SplineSect = RectBivariateSpline(np.arange(Sect.shape[-2]), np.arange(Sect.shape[-1]), Sect, kx = 2, ky = 2)
        SectDetailed = SplineSect(np.arange(0, Sect.shape[-2]-1, scale), np.arange(0, Sect.shape[-1]-1, scale), grid=True)
        yNew = MaxLoc[0]-range + np.argwhere(SectDetailed == np.max(SectDetailed))[0][0] * scale
        xNew = MaxLoc[1]-range + np.argwhere(SectDetailed == np.max(SectDetailed))[0][1] * scale

    return yNew ,xNew

def find_vortex_Min_center(vorticity, guass = 3, range = 3):
    """
    Finds the center of a vortex in a 2D velocity field using the vorticity field and interpolating the maxima location using a 2nd order bilinear polynomial fit at a resolution of 100* the original.

    Args:
        u: The x-component of the velocity field.
        v: The y-component of the velocity field.

    Returns:
        The center of the vortex, as a tuple of (x, y) coordinates.
    """
    scale = 0.05
    vortSmooth = ndimage.gaussian_filter(vorticity, guass)

    MinLoc = np.argwhere(vortSmooth == np.min(vortSmooth))[0]
    if MinLoc[0] < 5 or MinLoc[0] > vorticity.shape[0] - 5 or MinLoc[1] < 5 or MinLoc[1] > vorticity.shape[1] - 5:
        xNew, yNew = 0, 0
    else:
        Sect = vortSmooth[MinLoc[0]-range:MinLoc[0]+range+1, MinLoc[1]-range:MinLoc[1]+range+1]
        SplineSect = RectBivariateSpline(np.arange(Sect.shape[-2]), np.arange(Sect.shape[-1]), Sect, kx = 2, ky = 2)
        SectDetailed = SplineSect(np.arange(0, Sect.shape[-2]-1, scale), np.arange(0, Sect.shape[-1]-1, scale), grid=True)
        yNew = MinLoc[0]-range + np.argwhere(SectDetailed == np.min(SectDetailed))[0][0] * scale
        xNew = MinLoc[1]-range + np.argwhere(SectDetailed == np.min(SectDetailed))[0][1] * scale

    return  yNew ,xNew




def vorticityPeakTracking_inter(u, v, l = 0):
    """
    Finds the center of a vortex in a 2D velocity field using the vorticity field and interpolating the maxima location using a 2nd order bilinear polynomial fit at a resolution of 100* the original.
    It does this for each time step in a field of length u.shape[0]

    Args:
        u: The x-component of the velocity field.
        v: The y-component of the velocity field.

    Returns:
        The center of the vortex, as an array of (y, x) coordinates.
    """
    
    vorticity, vort_gauss = calculate_vorticity(u, v)
    VortLocMax = np.zeros((vort_gauss.shape[0], 2)) #same length in time as vorticity field, 2 rows - 0 for y, 1 for x
    VortLocMin = np.zeros((vort_gauss.shape[0], 2)) #same length in time as vorticity field, 2 rows - 0 for y, 1 for x

    if l == 0:
        l = vort_gauss.shape[0]
    elif l > vort_gauss.shape[0]:
        l = vort_gauss.shape[0]
    
    for i in range(l):
        vortTemp = vort_gauss[i, :, :]
        VortLocMax[i,:] = find_vortex_Max_center(vortTemp)
        VortLocMin[i,:] = find_vortex_Min_center(vortTemp)
    
    return VortLocMax, VortLocMin



def enstrophyPeakTracking(u, v, l = 0):
    """
     Finds the center of a vortex in a 2D velocity field using the local maximum enstrophy field.
    It does this for each time step in a field of length u.shape[0]

    Args:
        u: The x-component of the velocity field.
        v: The y-component of the velocity field.

    Returns:
        The center of the vortex, as an array of (y, x) coordinates.   
    """
    vorticity, vort_gauss = calculate_vorticity(u, v)
    enstrophy = np.square(vort_gauss)
    EnstLocMax = np.zeros((enstrophy.shape[0], 2)) #same length in time as enstrophy field, 2 rows - 0 for y, 1 for x

    if l == 0:
        l = enstrophy.shape[0]
    elif l > enstrophy.shape[0]:
        l = enstrophy.shape[0]
    
    for i in range(l):
        enstTemp = enstrophy[i, :, :]
        EnstLocMax[i,:] = np.argwhere(enstTemp == np.max(enstTemp))

    return EnstLocMax

def enstrophyPeakTracking_inter(u, v, l = 0):
    """
    Finds the center of a vortex in a 2D velocity field using the enstrophy field and interpolating the maxima location using a 2nd order bilinear polynomial fit at a resolution of 100* the original.
    It does this for each time step in a field of length u.shape[0]

    Args:
        u: The x-component of the velocity field.
        v: The y-component of the velocity field.

    Returns:
        The center of the peak enstrophy, as an array of (y, x) coordinates.
    """
    
    vorticity, vort_gauss = calculate_vorticity(u, v)
    enstrophy = np.square(vort_gauss)
    EnstLocMax = np.zeros((enstrophy.shape[0], 2)) #same length in time as vorticity field, 2 rows - 0 for y, 1 for x

    if l == 0:
        l = enstrophy.shape[0]
    elif l > enstrophy.shape[0]:
        l = enstrophy.shape[0]
    
    for i in range(l):
        EnstTemp = enstrophy[i, :, :]
        EnstLocMax[i,:] = find_vortex_Max_center(EnstTemp)

    return EnstLocMax

def Re(Upiston):
    d = 0.05  # Diameter of hole
    vk = 0.000001  # Kinematic viscosity
    Re = (Upiston/1000) * d / vk
    return Re


def animate_cube_contourf_line(
    cube_array, EnstLocMax, interval=17, cmap="seismic", save=0, output="line.mp4", fps=60, scale = 1, fsize = (10, 8), 
):

    """
    animates a numpy 3D Array for quick visualisation (specific to contourf). This function animates the velocity field with line indicating location of highest enstrophy.

    INPUT:
        cube_array  : name of 3D numpy array that needs to be animated.
        interval    : #of ms between each frame.
        cmap        : colormap. Default='seismic'

    OUTPUT:
        animated window going through the cube.

    """
    print("Start")
    fig, ax1 = plt.subplots(nrows = 1, ncols = 1, figsize=fsize, sharex = True, sharey = True)
    vmin = -np.max(np.abs(cube_array))
    vmax = np.max(np.abs(cube_array))
    def animate(i):
        ax1.clear()
        ax1.contourf(cube_array[i, :, :], cmap=cmap, levels = np.linspace(scale*vmin,scale*vmax,20))
        ax1.vlines(EnstLocMax[i,1], ymin = 0, ymax = (cube_array.shape[1]-1), colors='g', linestyles='dashed')
        ax1.scatter(EnstLocMax[i,1], EnstLocMax[i,0], color = 'k')
        ax1.set_title("%03d" % (i))
    print("2")
    anim = animation.FuncAnimation(
        fig, animate, frames=cube_array.shape[0], interval=interval, blit=False
    )

    if save == 0:
        plt.show()
    else:
        print("save loop")
        anim.save(output, writer="ffmpeg", fps=fps, dpi=160)


def TicTocGenerator():
    # Generator that returns time differences
    ti = 0  # initial time
    tf = time.time()  # final time
    while True:
        ti = tf
        tf = time.time()
        yield tf - ti  # returns the time difference


TicToc = TicTocGenerator()


def toc(tempBool=True):
    # Prints the time difference yielded by generator instance TicToc
    tempTimeInterval = next(TicToc)
    if tempBool:
        print("Elapsed time: %f seconds.\n" % tempTimeInterval)


def tic():
    # Records a time in TicToc, marks the beginning of a time interval
    toc(False)



def filterTankRPM(u,v,fps,rpm):
    filtfreq=(rpm*0.98)/60
    thresh = 0.015
    u_FFT = fft(u, axis=0)
    v_FFT = fft(v, axis=0)
    FFTFreq = fftfreq(u.shape[0], 1 / fps)
    mask1 = np.where(np.logical_and(filtfreq-thresh<FFTFreq, filtfreq+thresh>FFTFreq))
    mask2 = np.where(np.logical_and(-filtfreq-thresh<FFTFreq, -filtfreq+thresh>FFTFreq))

    u_FFT[mask1,:,:] = 0
    u_FFT[mask2,:,:] = 0
    v_FFT[mask1,:,:] = 0
    v_FFT[mask2,:,:] = 0

    u = ifft(u_FFT, axis=0)
    v = ifft(v_FFT, axis=0)
    u = np.real(u)
    v = np.real(v)
    return u, v

def filterTankRPM2(u,v,fps,rpm, rpmAdjust = 0.98):
    filtfreq=(rpm*rpmAdjust)/60
    filtfreq2=filtfreq*2
    thresh = 0.02
    u_FFT = fft(u, axis=0)
    v_FFT = fft(v, axis=0)
    FFTFreq = fftfreq(u.shape[0], 1 / fps)
    
    mask1 = np.where(np.logical_and(filtfreq-thresh<FFTFreq, filtfreq+thresh>FFTFreq))
    mask2 = np.where(np.logical_and(-filtfreq-thresh<FFTFreq, -filtfreq+thresh>FFTFreq))
    
    mask3 = np.where(np.logical_and(filtfreq2-thresh<FFTFreq, filtfreq2+thresh>FFTFreq))
    mask4 = np.where(np.logical_and(-filtfreq2-thresh<FFTFreq, -filtfreq2+thresh>FFTFreq))    

    window1 = np.zeros_like(FFTFreq)
    window1[mask1] = 1
    width = np.sum(window1)
    window1[mask1] = np.hanning(width)
    
    window2 = np.zeros_like(FFTFreq)
    window2[mask2] = 1
    window2[mask2] = np.hanning(width)

    window3 = np.zeros_like(FFTFreq)
    window3[mask3] = 1
    width2 = np.sum(window3)
    window3[mask3] = np.hanning(width2)

    window4 = np.zeros_like(FFTFreq)
    window4[mask4] = 1
    window4[mask4] = np.hanning(width2)

    maskT = mask1 + mask2 + mask3 + mask4
    windowT = window1 + window2 + window3 + window4

    u_FFT = u_FFT - u_FFT*windowT[:, None, None]
    # u_FFT[mask2,:,:] = u_FFT[mask2,:,:] - u_FFT[mask2,:,:]*window2[mask2, None, None]
    # v_FFT[mask1,:,:] = v_FFT[mask1,:,:] - v_FFT[mask1,:,:]*window1[mask1, None, None]
    v_FFT = v_FFT - v_FFT*windowT[:, None, None]

    u = ifft(u_FFT, axis=0)
    v = ifft(v_FFT, axis=0)
    u = np.real(u)
    v = np.real(v)
    return u, v

def FFT(Array, captureRate):
    """
    Uses Scipy real FFT function to give the frequencies and magnitudes of oscillations up to 1/2 of the sampling rate of the input data (fps). Abs value of spectra output.

    INPUT:
        Array       : 1D or 3D array containing velocity vectors over time.
        captureRate : The sampling rate of the data, this is usually fps. Do not input the frequency, instead number of samples per second. 

    OUTPUT:
        Fourier     : Magnitude of oscillations. 
        FFTfreq     : The frequency spectra correlating to the number of data points given and scaled using the sampling rate.

    """

    if Array.ndim == 1:
        Array = Array - np.mean(Array)
        Fourier = np.abs(rfft(Array))  # F[1:Array.shape[0]//2]
        FFTfreq = rfftfreq(Array.shape[0], 1 / captureRate)
        # FFTfreq = FFTfreq[1:Array.shape[0]//2]
    elif Array.ndim == 3:
        print('3D FFT')
        Array -= np.mean(Array, axis=0)
        Fourier = rfft(Array, axis=0)  # F[1:Array.shape[0]//2]
        FFTfreq = rfftfreq(Array.shape[0], 1 / captureRate)
        Fourier = np.mean(Fourier, axis=1)
        Fourier = np.mean(Fourier, axis=1)
        Fourier = np.abs(Fourier)
    return Fourier, FFTfreq


from decimal import Decimal

def TwoPtCorrIWs(Arr):
    ExX = Arr.shape[2]
    ExY = Arr.shape[1]
 
    nPairsHor = Decimal(math.factorial(ExX+2-1)// math.factorial(2) // math.factorial(ExX-1))
    nPairsVer = Decimal(math.factorial(ExY+2-1)// math.factorial(2) // math.factorial(ExY-1))

    nPairsHor = int(nPairsHor)
    nPairsVer = int(nPairsVer)

    print('end')
    # nPairsHor = 72911  # there are problems in this part of the code - this is a bodge for a single data set
    # nPairsVer = 337218 # there are problems in this part of the code - this is a bodge for a single data set
 
    corr_Hor = np.zeros(ExY * nPairsHor)
    dist_Hor = np.zeros(ExY * nPairsHor)
 
    corr_Ver = np.zeros(ExX * nPairsVer)
    dist_Ver = np.zeros(ExX * nPairsVer)
 
    for i in range(ExY):
        for pair, indexi in zip(itertools.combinations_with_replacement(range(ExX), 2), range(nPairsHor)):
            corr_Hor[indexi+i*nPairsHor] = np.dot(Arr[:,i,pair[0]], Arr[:,i,pair[1]])
            dist_Hor[indexi+i*nPairsHor] = abs(pair[0] - pair[1])
 
    for j in range(ExX):
        for pair, indexj in zip(itertools.combinations_with_replacement(range(ExY), 2), range(nPairsVer)):
            corr_Ver[indexj+j*nPairsVer] = np.dot(Arr[:,pair[0],j], Arr[:,pair[1],j])
            dist_Ver[indexj+j*nPairsVer] = abs(pair[0] - pair[1])
 
    distH, corrH = f_dict(dist_Hor, corr_Hor)
    distV, corrV = f_dict(dist_Ver, corr_Ver)
    corrH = corrH/corrH[0]
    corrV = corrV/corrV[0]
 
    XC = FindFirstIntercept(corrH)
    YC = FindFirstIntercept(corrV)
 
    Angle = np.round(np.degrees(np.arctan(YC/XC)), 3)
 
    return distH, distV, corrH, corrV, XC, YC, Angle


def f_dict(listA, listB):
 
    """
    Averages listB values with corresponding identical listA values.
    
    Parameters
    ----------
    listA : list
        List of 'keys' which form catagories.
 
    listB : list
        List of corresponding data to be averaged.
 
    Returns
    -------
    distances : list
        List of concatenated keys.
 
    avg : list
        List of corresponding average values.
 
    """
    d = {}
 
    for a, b in zip(listA, listB):
        d.setdefault(a, []).append(b)
 
    avg = []
    for key in d:
        avg.append(sum(d[key])/len(d[key]))
    distances = list(d.keys())
 
    return distances, avg



def FindFirstIntercept(Corr):
    """
    Linearly interpolates the point of first intercept with y=0 on a graph.
    
    Parameters
    ----------
    Corr : list
        List of values for which to find intercept
 
    Returns
    -------
    interpolatedValue : float
        x value at which y = 0.
 
    """
 
    Corr = np.array(Corr)
    CorrLess = np.where(Corr<0)
    CorrLess = CorrLess[0]
 
    if len(CorrLess) == 0:
        interpolatedValue = np.nan
    else:
        n_neg = CorrLess[0]
        neg_values = np.array([[n_neg-1, n_neg], [Corr[n_neg-1], Corr[n_neg]]])
        difference = neg_values[1,0]/(neg_values[1,0] - neg_values[1,1])
        interpolatedValue = neg_values[0,0] + difference
 
    return interpolatedValue


def KECalc(u, r):
    Values = 2 * np.pi * 0.5 * u**2 * r
    IntVals = np.zeros(u.shape[0])
    for j in range(u.shape[0]):
        plt.plot(r, Values[j, :])
        IntVals[j] = integrate.simpson(r, Values[j, :])
        plt.show()
    totalKE = np.sum(IntVals)


def FindPowerLaw(x, y):
    # is x = y^coeff[0]
    if np.any(y < 0):
        print("Negative values encountered finding power law")
    logx = np.log(x)
    logy = np.log(y)
    coeffs = np.polyfit(logx, logy, deg=1)
    poly = np.poly1d(coeffs)
    line = np.exp(poly(np.log(x)))
    # line = np.exp(coeffs[0]*np.log(x) + coeffs[1])
 
    return line, coeffs

def loglogplot(axP, x, y, col, rpm, ann = 1):
    axP.loglog(
    x,
    y,
    color=col,
    linestyle="None",
    marker=".",
    label="RPM - {}".format(rpm),
    )
    if ann == 1:
        l, co = FindPowerLaw(x, y)
        axP.loglog(x, l, color='k', linestyle="dotted")
        axP.annotate(str(np.round(co[0], 3)), (x[-1], l[-1]))
    else:
        pass

def InterpZeros(y):
    if (y == 0).any() == True:
        y = np.array(y)
        x = np.arange(y.shape[0])
        idx = np.nonzero(y)
        f = interp1d(x[idx], y[idx], fill_value="extrapolate")
        ynew = f(x)
    else:
        ynew = y
    return ynew 

def legendy(ax, loc='best'):
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc=loc)

def load_multiple_rings(Dir, n = 10):
    # u, v = oj.importData73(str(Dir) + "1/Data/PIV_export_fine.mat")
    u, v = oj.importData73(str(Dir) + "1/Data/PIV_export.mat")
    print(str(Dir), "\r")
    u = np.zeros([n, u.shape[0], u.shape[1], u.shape[2]])
    v = np.zeros([n, v.shape[0], v.shape[1], v.shape[2]])

    for i in range(1, n+1):
        # u[(i-1),:,:,:], v[(i-1),:,:,:] = oj.importData73(str(Dir) + str(i) + "/Data/PIV_export_fine.mat")
        u[(i-1),:,:,:], v[(i-1),:,:,:] = oj.importData73(str(Dir) + str(i) + "/Data/PIV_export.mat")
        u[(i-1),:,:,:], v[(i-1),:,:,:] = oj.scaleVelNozzle(u[(i-1),:,:,:], v[(i-1),:,:,:], 90)
        oj.progressBar(i, n)

    return u, v

def calculate_divergence(u, v):
    """
    calculates divergence of velocity field
     
    INPUT:
        u           : 3D Numpy tensor containing velocity data
        v           : 3D Numpy tensor containing velocity data

    OUTPUT:
        divergence   : 3D Numpy tensor containing divergence data
        divergence_gauss : 3D Numpy tensor containing divergence data after a gausian filter

    """
    du = np.gradient(u, axis = 2)
    dv = np.gradient(v, axis = 1)
    divergence = du + dv
    divergence_gauss = gaussian_filter(divergence, sigma = 0.7)
    return divergence, divergence_gauss

def thesis_plot_settings():
    settings = {
        'figure.figsize': (5.5, 4),
        'font.size': 12,
        'lines.linewidth': 2,
        'axes.labelsize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 10,
        'figure.dpi': 400,
        'figure.constrained_layout.use': True
    }
    plt.rcParams.update(settings)
