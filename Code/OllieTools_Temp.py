import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.interpolate import interp1d

def animate_cube_quiver_magn(

    cube_array1,
    cube_array2,
    interval=75,
    cmap="bwr",
    save=0,
    output="output.mp4",
    fps=12,
):
 
    """
    animates a numpy 3D Array for quick visualisation (specific to quiver).
 
    INPUT:
        cube_array1  : name of 3D numpy array that needs to be animated.
        cube_array2  : name of 3D numpy array that needs to be animated.
        interval    : #of ms between each frame.
        cmap        : colormap. Default='bwr'
 
    OUTPUT:
        animated window going through the cube.
 
    """
    proportion =  cube_array1.shape[2] / cube_array1.shape[1]
    fig, ax = plt.subplots(figsize=(6, 6*proportion))
    vmin = -np.max(np.abs(cube_array1 ** 2 + cube_array2 ** 2))
    vmax = np.max(np.abs(cube_array1 ** 2 + cube_array2 ** 2))
    levels = np.linspace(vmin,vmax,20)
    Cont = ax.contourf(np.sqrt(cube_array1[0, :, :] ** 2 + cube_array2[0, :, :] ** 2),levels = levels , cmap=cmap)
    cbar = fig.colorbar(Cont)
    # cbar.ax.set_ylabel('verbosity coefficient')
    def animate(i):
        ax.clear()
        ax.contourf(np.sqrt(cube_array1[i, :, :] ** 2 + cube_array2[i, :, :] ** 2),levels = levels , cmap=cmap)
        ax.quiver(cube_array1[i, :, :], cube_array2[i, :, :])
       
        ax.set_title("%03d" % (i))
   
    ani = animation.FuncAnimation(
        fig, animate, frames=cube_array1.shape[0], interval=interval, blit=False
    )
 
    # plt.colorbar()
    if save == 0:
        plt.show()
    else:
        ani.save(output, writer="ffmpeg", fps=fps, dpi=160)


def progressBar(step,nSteps, width=40):
 
    percent = int(np.ceil(step*100/nSteps))
 
    left = width * percent // 100
    right = width - left
   
    tags = "#" * left
    spaces = " " * right
    percents = f"{percent:.0f}%"
   
    print("\r[", tags, spaces, "]", percents, sep="", end="", flush=True)
 
 
def NDUnitsForPlots(shapeX, shapeY, widthM = 0.268, HeightM = 0.4, jetLocPix = 694, pixX = 1328, d = 0.006):
    shapeX = shapeX -1
    zeroPos = int(jetLocPix/pixX * shapeX)
 
    r = np.linspace(-widthM * zeroPos/shapeX, widthM * (shapeX-zeroPos)/shapeX, shapeX+1)
    r_nd = r / d
 
    z = np.linspace(0, HeightM, shapeY)
    z_nd = z / d
 
    return r_nd, z_nd
 
 
def InterpZeros(y):
    if (y==0).any() == True:
        y = np.array(y)
        x = np.arange(y.shape[0])
        idx = np.nonzero(y)
        f = interp1d(x[idx], y[idx], fill_value="extrapolate")
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
    cube_array, VortLocMax, VortLocMin, interval=17, cmap="bwr", save=0, output="points.mp4", fps=60, scale = 1, fsize = (10, 8), 
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
        ax1.plot([x1,x2],[y1,y2], "--", linewidth=2.0)
        ax1.set_title("%03d" % (i))
    print("2")
    anim = animation.FuncAnimation(
        fig, animate, frames=cube_array.shape[0], interval=interval, blit=False
    )

    if save == 0:
        plt.show()
    # else:
    #     print("save loop")
    #     anim.save(output, writer="ffmpeg", fps=fps, dpi=160)

    writervideo = animation.FFMpegWriter(fps=60)
    anim.save(output, writer=writervideo, dpi=160)

    anim.save(output, writer="ffmpeg", fps=fps, dpi=160)

def animate_cube_contourf(
    cube_array, interval=17, cmap="bwr", save=0, output="output.mp4", fps=60, scale = 1, fsize = (10, 8)
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
    print("Start")
    fig, ax = plt.subplots(figsize=fsize)
    vmin = -np.max(np.abs(cube_array))
    vmax = np.max(np.abs(cube_array))
    def animate(i):
        ax.clear()
        ax.contourf(cube_array[i, :, :], cmap=cmap, levels = np.linspace(scale*vmin,scale*vmax,20))
        ax.set_title("%03d" % (i))
    print("2")
    anim = animation.FuncAnimation(
        fig, animate, frames=cube_array.shape[0], interval=interval, blit=False
    )
    print("3")
    # plt.colorbar()
    if save == 0:
        plt.show()
    # else:
    #     print("save loop")
    #     anim.save(output, writer="ffmpeg", fps=fps, dpi=160)

    writervideo = animation.FFMpegWriter(fps=60)
    anim.save(output, writer=writervideo, dpi=160)

    anim.save(output, writer="ffmpeg", fps=fps, dpi=160)
    print("end")