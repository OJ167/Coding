from scipy import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from numpy.fft import fft, fftfreq, irfft, rfft2, rfft, rfftfreq
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from datetime import date
from os import path
import os
import math
import itertools
import scipy.ndimage
from scipy.interpolate import interp1d

#Define global variables 
u = [[[]]]
v = [[[]]]
x_size = []
y_size = []

#Create main GIU window
root = Tk()
root.title('PIV Analysis ')
root.geometry('1270x900')

####################################################### Define variables to change using options tabs ################################################

Label(root, text = "Table RPM:").grid(row = 3, column = 0)
TRPMEntry= Entry(root)
TRPMEntry.grid(row=3,column=1, sticky="w")

Label(root, text = "Pump RPM:").grid(row = 4, column = 0)
PRPMEntry= Entry(root)
PRPMEntry.grid(row=4,column=1, sticky="w")

Label(root, text = "Camera FPS:").grid(row = 5, column = 0)
FPSEntry= Entry(root)
FPSEntry.grid(row=5,column=1, sticky="w")

Label(root, text = "Extra notes:").grid(row = 6, column = 0)
NotesEntry= Entry(root)
NotesEntry.grid(row=6,column=1, sticky="ew")

# Extra Variables
t = "JET"           # Type of experiment
d = 0.006           # Diameter of hole
v = 0.000001        # Kinematic viscosity
x = 0.000195        # Conversion factor from rpm(motor) to l/s 
l = 0.08            # Characteristic length
notes = "Experiment conducted to attempt to recreate condtitions for formation breakdown of jet in rotating flow"


######################################################### Create directory and folder #########################################################



def CheckEntries():
    # Check if all entries contain a number
    if len(TRPMEntry.get()) == 0:
        updateText('Please provide Table RPM')
    else:
        if len(PRPMEntry.get()) == 0:
            updateText('Please provide Motor RPM')
        else:
            if len(FPSEntry.get()) == 0:
                updateText('Please provide Camera FPS')
            else:
                return(1)

    
def MoveAndCatalogue():
    global number
    entries = CheckEntries()
    if entries == 1:
        # Get todays date and convert to string
        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        # Set root directory
        directoryNew = filedialog.askdirectory()
        # Create directory within root with todays date 
        path1 = os.path.join(directoryNew, d1)
        if path.exists(path1) == True:
            pass
        else:
            os.mkdir(path1) 
        Name = str('RPM-'+str(TRPMEntry.get())+'_Pump-'+str(PRPMEntry.get())+'_FPS-'+str(FPSEntry.get()) + "_" + t)
        # Create containing folder with basic details
        folder = os.path.join(path1,Name)
        if path.exists(folder) == True:
            pass
        else:  
            os.mkdir(folder) 
        # Create final numbered containers - by counting up by one from currently existing folder  
        number = str(1)
        def count():
            global number
            if path.exists(os.path.join(folder, number)) == True:
                number = str(int(number) + 1)
                count()
            else:  
                os.mkdir(os.path.join(folder, number))    
        count()
        print(number)
        final = os.path.join(folder, number)

        os.mkdir(os.path.join(final, 'Images'))
        os.mkdir(os.path.join(final, 'Data'))

        # Calculations
        Omega = 2 * math.pi * float(TRPMEntry.get()) / 60 
        Q = (float(PRPMEntry.get()) * x)/(1000)
        U0 = (4 * Q) / (math.pi * d**2)
        Re = U0 * d / v
        Ek = v / (2 * Omega * l**2)
        Ro = U0 / (Omega * d)
        # Create Text file with required variables 
        file1 = open(os.path.join(final, "Details.txt"),"w+")
        file1.write("Basic variables." + "\n" + "\n")
        file1.write("   - Table RPM  =  " + str(TRPMEntry.get()) + "\n")
        file1.write("   - Pump RPM  =  " + str(PRPMEntry.get()) + "\n")
        file1.write("   - FPS Camera  =  " + str(FPSEntry.get()) + "\n" + "\n" + "Calculated variables."+ "\n" + "\n")
        file1.write("   - Omega = " + str(round(Omega,3)) + " rad/s" + "\n")
        file1.write("   - Q = " + str(round(Q,9)) + " m^3/s = " + str(round(Q*1000,6)) + " l/s " + str(round(Q*1000000,9)) + " cm^3/s"+ "\n")
        file1.write("   - U = " + str(round(U0,5)) + " m/s" + "\n")
        file1.write("   - Re = " + str(round(Re,5)) + "\n")
        file1.write("   - Ro = " + str(round(Ro,5)) + "\n")
        file1.write("   - Ek = " + str(round(Ek,9)) + "\n" + "\n" + "Notes." + "\n")
        file1.write(notes + "\n")
        file1.write(str(NotesEntry.get()))
        file1.close()
    else:
        pass

MoveFileButton = Button(root, text='Create Folder', command=MoveAndCatalogue)
MoveFileButton.grid(row=6,column=2)

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


######################################################### Plot canvas for graph #########################################################


f = Figure(figsize=(6.4,8.2), dpi=100)
plot_frame = Frame(root, bd=-2)
plot_frame.grid(row=2, column=4, rowspan=50)

canvas = FigureCanvasTkAgg(f, plot_frame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2Tk(canvas,plot_frame)
toolbar.update()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

######################################################### Find Directory and load values into app #########################################################
 

directoryEntry= Entry(root)
directoryEntry.grid(row=1,column=1, ipadx=120)

def directoryClick():
    directory = filedialog.askopenfilename()
    directoryEntry.delete(0,END)
    directoryEntry.insert(0, directory)

root.grid_rowconfigure(0, minsize=20)
directoryButton = Button(root, text='Choose File', command=directoryClick)
directoryButton.grid(row=1,column=0)

#1 for filtered, 0 for original
dataSource = IntVar()
Radiobutton(root, text = "Original", variable = dataSource, value = 1).grid(row = 2, column = 2)
Radiobutton(root, text = "Filtered", variable = dataSource, value = 0).grid(row = 3, column = 2)
Radiobutton(root, text = "Split", variable = dataSource, value = 2).grid(row = 4, column = 2)

def updateText(msg):
    alertBox.config(state=NORMAL)
    alertBox.delete(1.0,END)
    alertBox.insert(INSERT, msg)
    alertBox.config(state=DISABLED)

Label(root, text = "Alerts:").grid(row = 50, column = 0)
alertBox = Text(root,state = DISABLED, height = 1, width = 40)
alertBox.grid(row = 50, column = 1)

def ImportRaw():
    global u,v,x,y,dataSource
    file_ext = os.path.splitext(directoryEntry.get())
    if os.path.exists(directoryEntry.get()) == FALSE:
        updateText("That file does not exist")
    elif file_ext[1] != ".mat":
        updateText("Please choose a .mat data file")
    else:
        os.chdir(os.path.dirname(directoryEntry.get()))
        mat_contents = io.loadmat(os.path.basename(directoryEntry.get()))
        #1 for filtered, 0 for original
        #print("dataSource =",dataSource.get())
        if dataSource.get() == 0:
            u_temp = np.squeeze(mat_contents['u_filtered']) 
            v_temp = np.squeeze(mat_contents['v_filtered'])
            print("Filtered Data Imported")
            updateText("Filtered data read & cleaned successfully")
        elif dataSource.get() == 1:
            u_temp = np.squeeze(mat_contents['u_original']) 
            v_temp = np.squeeze(mat_contents['v_original'])
            print("Orignal Data Imported")
            updateText("Original data read & cleaned successfully")
        elif dataSource.get() == 2:
            u_temp = np.squeeze(mat_contents['u_filtered']) 
            v_temp = np.squeeze(mat_contents['v_filtered'])
            split_level = u_temp[0].shape[0]
            
            for i in range(u_temp.shape[0]):
                u_temp[i] = u_temp[i][0:(math.floor(split_level/2)),:]
            for i in range(v_temp.shape[0]):
                v_temp[i] = v_temp[i][0:(math.floor(split_level/2)),:]
            print("Filtered Data Imported and Split")
            updateText("Filtered data read & cleaned successfully")
        u = np.empty((u_temp.shape[0], u_temp[0].shape[0], u_temp[0].shape[1]))
        for i in range(u.shape[0]):
            u[i] = u_temp[i]
        print("u data cleaned")
        v = np.empty((v_temp.shape[0], v_temp[0].shape[0], v_temp[0].shape[1]))
        for i in range(v.shape[0]):
            v[i] = v_temp[i]
        print("v data cleaned")
        if u.shape == v.shape:
            sizeLabelx = Label(root, text=v.shape)
            sizeLabelx.grid(row=1,column=4)
        # u[3][2][1] refers to the entry 3rd row of the 2nd column in the 4th page
        # Remember that matlab counts e.g. from 1-100 whereas python counts 0-99

def rotate():
    global u, v
    u_temp = np.rot90(u, axes=(1,2))
    v_temp = np.rot90(v, axes=(1,2))
    v = - u_temp
    u = - v_temp 

def cleanData(a):
    a_list = [table for table in a]
    a_np = np.array(a_list)
    [a_timesteps,a_columns,a_rows] = a_np.shape
    for i in range(a_timesteps):
        for j in range(a_columns):
            for k in range(a_rows):
                if (np.isnan(a_np[i][j][k]) == TRUE):
                    #a_np[i][j][k] = "{0:.10f}".format(a_np[i][j][k])

                    a_np[i][j][k] = 0
                    #print(a_np[i][j][k])
                    #print("i = ",i)
                    #print("j =" , j)
                    #print("k =" , k)
                    #print("")

    return a_np

directoryButton = Button(root, text='Import', command=ImportRaw, padx=15).grid(row=1,column=2 )

rotateButton = Button(root, text='Rotate', command=rotate, padx=15).grid(row=1,column=3 )


######################################################### Create Tabs to house settings for individual controls ##########################################################


tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Average')
tabControl.grid(row=9, column=0, columnspan = 3, sticky='ew')
blankt1 = Label(tab1, text=" ")
blankt1.grid(row=0, column=0)

tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text='2 Pt Correlation')
blankt2 = Label(tab2, text=" ")
blankt2.grid(row=0, column=0)

tab3 = ttk.Frame(tabControl)
tabControl.add(tab3, text='Vertical IW Visualisation')
blankt3 = Label(tab3, text=" ")
blankt3.grid(row=0, column=0)

tab4 = ttk.Frame(tabControl)
tabControl.add(tab4, text='2 Pt, Method 2')
blankt4 = Label(tab4, text=" ")
blankt4.grid(row=0, column=0)

tab5 = ttk.Frame(tabControl)
tabControl.add(tab5, text='Zone Tracking')
blankt5 = Label(tab5, text=" ", padx=15)
blankt5.grid(row=0, column=0)

################################################################# General Functions for use throughout ##############################################

def plotCanvasFull():
    f.subplots_adjust(bottom=0.005, top=0.995, left=0.01, right=0.99)
    canvas.draw()
    canvas.get_tk_widget().pack()

def plotCanvasAxes():
    f.subplots_adjust(bottom=0.08, top=0.98, left=0.13, right=0.98)
    canvas.draw()
    canvas.get_tk_widget().pack()


################################################################# Function 1 - Average Plots ########################################################

def AverageCalc():
    u1 = np.mean(u, axis=0)
    v1 = np.mean(v, axis=0)
    a = np.arange(0,u.shape[2],1)
    b = np.arange(0,u.shape[1],1)
    mag = np.sqrt(u1**2 + v1**2)
    A , B = np.meshgrid(a,b)
    f.clear()
    quiv = f.add_subplot(111)
    quiv.quiver(A,B,u1,v1,mag)
    quiv.xaxis.set_ticks([])
    quiv.yaxis.set_ticks([])
    quiv.plot()
    plotCanvasFull()
    updateText('Displaying Average Velocity Plot')


but1t1 = Button(tab1, text='Plot', command=AverageCalc,  padx=15)
but1t1.grid(row=2,column=2 )

def LinePlotCalc():
    n = IntVar(0,8)
    n.set(ent1t1.get())
    LineScale = DoubleVar(0,8)
    LineScale.set(ent2t1.get())
    u1 = np.mean(u, axis=0)
    v1 = np.mean(v, axis=0)
    zeros = np.full_like(v1,0)
    for i in range(v1.shape[0]):
        if((i % n.get()) != 0):
            v1[i,:] = 0
    f.clear()
    val = f.add_subplot(111)
    c = np.arange(0,v1.shape[1],1)
    d = np.arange(0,v1.shape[0],1)
    C , D = np.meshgrid(c,d)
    val.quiver(C,D,zeros,v1,angles='xy', scale_units='xy', scale=(1/(n.get()*LineScale.get())))
    val.xaxis.set_ticks([])
    val.yaxis.set_ticks([])
    val.plot()
    plotCanvasFull()
    updateText('Displaying Validation Line Plot')

def TransImg():
    if CheckEntries() == 1:
        fps = IntVar(0,60)
        fps.set(FPSEntry.get())
        f.clear()
        for t in range(1*fps.get(), 5*fps.get(), 1*fps.get()):
            mag = np.sqrt(u[t,:,:]**2 + v[t,:,:]**2)
            ax = f.add_subplot(2, 2, int(t/fps.get()))
            a = np.arange(0,u.shape[2],1)
            b = np.arange(0,u.shape[1],1)
            A , B = np.meshgrid(a,b)
            #ax.quiver(A,B,u[t,:,:], v[t,:,:],mag)
            ax.contourf(A,B, mag)
            ax.xaxis.set_ticks([])
            ax.yaxis.set_ticks([])
            ax.plot()
        plotCanvasFull()
    else:
        pass

def TransientLine(z=[[[]]]):
    #inputs
    p1_x = 0
    p1_y = 15
    p2_x = z.shape[1]    
    p2_y = 15
    spacing = 150
    int_x, int_y  = np.linspace(p1_x, p2_x, spacing), np.linspace(p1_y, p2_y, spacing)
    zi = []
    for time in range(z.shape[0]):
        zi.extend(scipy.ndimage.map_coordinates(z[time,:,:], np.vstack((int_x,int_y))))
    overTime = np.array(zi).reshape((z.shape[0], spacing))

    f.clear()
    ax = f.add_subplot(111)
    a = np.arange(0,spacing,1)
    b = np.arange(0,z.shape[0],1)
    A , B = np.meshgrid(a,b)
    ax.contourf(A,B,overTime, 40, cmap='seismic')
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])
    ax.plot()
    plotCanvasFull()



def LineOnAverage():
    TransientLine(v)

Label(tab1, text=" ", padx=25).grid(row=0, column=4)

label1t1 = Label(tab1, text="Number of inactive rows: ")
label1t1.grid(row=1, column=5)
ent1t1 = tk.Entry(tab1)
ent1t1.grid(row=2, column=5, columnspan=2)
ent1t1.insert(0, 8)

label2t1 = Label(tab1, text="Line scale: ")
label2t1.grid(row=3, column=5)
ent2t1 = tk.Entry(tab1)
ent2t1.grid(row=4, column=5, columnspan=2)
ent2t1.insert(0, 0.7)

but2t1 = Button(tab1, text='Line Plot', command=LinePlotCalc, padx=15)
but2t1.grid(row=5,column=5 )

but3t1 = Button(tab1, text='Plot Transient', command=TransImg, padx=15)
but3t1.grid(row=4,column=2 )

but4t1 = Button(tab1, text='Plot Transient Line', command=LineOnAverage, padx=15)
but4t1.grid(row=6,column=2 )


################################################################# Function 2 - 2 Point ########################################################


convolution_V = []
distance = []
angle = []
conv1  = []
dist1  = []
ang1  = []
conv2  = []
dist2 = []
ang2  = []

def f_dict(listA, listB):
    d = {}

    for a, b in zip(listA, listB):
        d.setdefault(a, []).append(b)

    avg = []
    for key in d:
        avg.append(sum(d[key])/len(d[key]))
    distance_keys = list(d.keys())

    return distance_keys, avg

def twoPointCorrTime(v_imput = [[[]]]):
    print(v_imput.shape)

    convolution_V = []
    distance = []
    angle = []

    a = np.arange(0,v_imput.shape[2]*v_imput.shape[1],1)
    out = np.array(np.meshgrid(a,a), dtype=float).T.reshape(-1,2)
    b = np.arange(0, v_imput.shape[1], 1)
    c = np.arange(0, v_imput.shape[2], 1)
    Grid = np.array(np.meshgrid(b,c))

    v_long = v_imput.copy().reshape(v_imput.shape[0],(v_imput.shape[2]*v_imput.shape[1]))

    v_long_norm = v_long/(np.max(v_long))


    for P1 in range(0, out.shape[0]): 
        if out[P1,1] < out[P1,0]:
            convolution_V.append(0)
            distance.append(0)
            angle.append(0)
        elif out[P1,1] == out[P1,0]:
            convolution_V.append(0)
            distance.append(0)
            angle.append(0)
        else:
            if (int(out[P1,0]) % 100) == 0 and int(out[P1,1]) == int(a.shape[0]-1):
                print(str(math.floor(100* (int(out[P1,0]) /  int(a.shape[0]-1)))) + '%')
            else:
                pass

            v_long_temp1 = v_long_norm[ :, int(out[P1,0])]
            v_long_temp2 = v_long_norm[ :, int(out[P1,1])]
            
            #corr_result_temp = signal.correlate(u_long_temp1, u_long_temp2)

            corr_result_temp = np.dot(v_long_temp1, v_long_temp2)           
            convolution_V.append(int(corr_result_temp))
            

            PointA = np.array((int(out[P1,0] % v_imput.shape[2]), int(math.floor(out[P1,0]/v_imput.shape[2]))))
            PointB = np.array((int(out[P1,1] % v_imput.shape[2]), int(math.floor(out[P1,1]/v_imput.shape[2]))))
            dist_temp = np.linalg.norm(PointA-PointB)
            angle_temp = np.rad2deg(math.atan2(PointA[1]-PointB[1], PointA[0]-PointB[0]))
            distance.append(dist_temp)
            angle.append(angle_temp)
    autocorr_V = np.dot(v_long_norm[ :, 0],v_long_norm[ :, 0])
    convolution_V_array = np.array(convolution_V)/int(autocorr_V)
    convolution_V = convolution_V_array.tolist()
    return convolution_V, distance, angle

def filterTwoPointCorr(corr_values = [], distance_values = [], angle_values = []): #convolution_V, distance, angle
    input_angle = int(ent1t2.get())
    width = int(ent2t2.get())

    filtered_Distances = []
    filtered_Corr = []

    for P1 in range(0, len(angle_values) ): 
        if LeftRight.get() == 0:
            if (90 - (input_angle + width)) <= angle_values[P1] <= (90 - (input_angle - width)):
                filtered_Distances.append(distance_values[P1])
                filtered_Corr.append(corr_values[P1])
            elif (-90 - (input_angle + width)) <= angle_values[P1] <= (-90 - (input_angle - width)):
                filtered_Distances.append(distance_values[P1])
                filtered_Corr.append(corr_values[P1])            
            else:
                pass
        if LeftRight.get() == 1:
            if (-90 + (input_angle - width)) <= angle_values[P1] <= (-90 + (input_angle + width)):
                filtered_Distances.append(distance_values[P1])
                filtered_Corr.append(corr_values[P1])
            elif (90 + (input_angle - width)) <= angle_values[P1] <= (90 + (input_angle + width)):
                filtered_Distances.append(distance_values[P1])
                filtered_Corr.append(corr_values[P1])            
            else:
                pass
    
    max_value = max(filtered_Corr)
    filtered_Corr = np.array(filtered_Corr)/max_value

    DistCorrData = f_dict(filtered_Distances,filtered_Corr)

    return DistCorrData

def single2Pt():
    twoPointCorrTime(v)

def single2PtPlot():
    DistCorrData = filterTwoPointCorr(convolution_V, distance, angle)
    f.clear()
    ax = f.add_subplot(111)
    ax.scatter(DistCorrData[0], DistCorrData[1])    
    #ax.xaxis.set_ticks([])
    #ax.yaxis.set_ticks([])
    ax.set(xlabel='Distance between Points', ylabel='Magnitude of Correlation')
    ax.plot()
    plotCanvasAxes()
    updateText('Displaying Vertical IW Visualisation')

def Run2Pt():
    global conv1, dist1, ang1, conv2, dist2, ang2

    filterValue = float(ent3t5.get())
    v_trimmed = v.copy()
    v_trimmed[v_trimmed > filterValue] = 1
    v_trimmed[v_trimmed < filterValue] = 0
    v_trimmed_average = np.mean(v_trimmed, axis =1)
    v_trimmed_average = np.mean(v_trimmed_average, axis =1)
    v_trimmed_average_smoothed = []
    A = 30
    for i in range(math.floor(len(v_trimmed_average)/A)):
        v_trimmed_average_smoothed_mag = np.mean(v_trimmed_average[A*(i):A*(i+1)])
        v_trimmed_average_smoothed.append(v_trimmed_average_smoothed_mag)

    filterValue2 = max(v_trimmed_average_smoothed)/20
    Block = np.array(v_trimmed_average_smoothed.copy())
    Block[Block > filterValue2] = 1
    Block[Block < filterValue2] = 0
    

    for j in range(1,(len(Block)-1)):
        if Block[j] != Block[j-1] and Block[j] != Block[j+1]:
            Block[j] = Block[j+1]
        else:
            pass

    jetV = np.empty((1, v.shape[1], v.shape[2]))
    noJetV = np.empty((1, v[0].shape[0], v[0].shape[1]))
    #print(jetV.shape)
    #print(np.transpose(np.atleast_3d(v[1,:,:]), (2, 0, 1)).shape)

    for k in range(v.shape[0]-A):
        if Block[math.floor(k/A)] == 1:
            jetV = np.concatenate((jetV, np.transpose(np.atleast_3d(v[k,:,:]), (2, 0, 1))))
        else:
            noJetV = np.concatenate((noJetV, np.transpose(np.atleast_3d(v[k,:,:]), (2, 0, 1))))   
    jetV = jetV[1:,:,:]
    noJetV = noJetV[1:,:,:]

    conv1, dist1, ang1 = twoPointCorrTime(jetV)
    print('Jet data computed')
    conv2, dist2, ang2 = twoPointCorrTime(noJetV)
    print('No jet data computed')
    updateText('Data sorted - ' + str(jetV.shape[0]) + ':' + str(noJetV.shape[0]))

def double2PtPlot():
    DistCorrDataJet = filterTwoPointCorr(conv1, dist1, ang1)
    DistCorrDataNoJet = filterTwoPointCorr(conv2, dist2, ang2)
    f.clear()
    ax = f.add_subplot(1, 1, 1)
    ax.plot(DistCorrDataJet[0], DistCorrDataJet[1], 'xb--', label = 'Jet')    
    ax.plot(DistCorrDataNoJet[0], DistCorrDataNoJet[1], 'xr--', label = 'Suppressed')  
    ax.set(xlabel='Distance between Points', ylabel='Magnitude of Correlation')
    ax.plot()
    ax.legend(loc="upper right")
    plotCanvasAxes()
    updateText('Displaying Filtered 2Pt Corr Data')

def double2PtPlotTotal():
    DistCorrDataJet = f_dict(dist1,conv1)
    DistCorrDataNoJet = f_dict(dist2,conv2)
    f.clear()
    ax = f.add_subplot(1, 1, 1)
    ax.plot(DistCorrDataJet[0], DistCorrDataJet[1], 'xb', label = 'Jet')    
    ax.plot(DistCorrDataNoJet[0], DistCorrDataNoJet[1], 'xr', label = 'Suppressed')  
    ax.legend(loc="upper right")
    ax.set(xlabel='Distance between Points', ylabel='Magnitude of Correlation')
    ax.plot()
    plotCanvasAxes()
    updateText('Displaying Total 2Pt Corr Data')


Label(tab2, text=" ", padx=25).grid(row=1, column=1)
Label(tab2, text=" ", padx=25, pady=10).grid(row=6, column=0)

label1t2 = Label(tab2, text="Filtering angle: ")
label1t2.grid(row=2, column=0, sticky="w")
ent1t2 = tk.Entry(tab2)
ent1t2.grid(row=3, column=0 , sticky="ew")
ent1t2.insert(0, 45)

label2t2 = Label(tab2, text=" Width of filter: ")
label2t2.grid(row=4, column=0, sticky="w")
ent2t2 = tk.Entry(tab2)
ent2t2.grid(row=5, column=0, sticky="ew")
ent2t2.insert(0, 0)

Label(tab2, text=" ", padx=25).grid(row=0, column=2)
LeftRight = IntVar()
Radiobutton(tab2, text = "Right", variable = LeftRight, value = 1).grid(row = 2, column = 3)
Radiobutton(tab2, text = "Left", variable = LeftRight, value = 0).grid(row = 3, column = 3)

but1t2 = Button(tab2, text='Calculate single', command=single2Pt, padx=15)
but1t2.grid(row=7,column=0 , sticky="ew")

but2t2 = Button(tab2, text='Plot single', command=single2PtPlot, padx=15)
but2t2.grid(row=8,column=0, sticky="ew" )

but1t2 = Button(tab2, text='Calculate 2 Phase', command=Run2Pt, padx=15)
but1t2.grid(row=7,column=2 , sticky="ew")

but1t2 = Button(tab2, text='Plot 2 Phase', command=double2PtPlot, padx=15)
but1t2.grid(row=8,column=2 , sticky="ew")

but1t3 = Button(tab2, text='Plot Total 2 Phase', command=double2PtPlotTotal, padx=15)
but1t3.grid(row=9,column=2 , sticky="ew")


################################################################# Function 3 - Basic IW Visualisation ########################################################


def PhaseAv():
    if CheckEntries() == 1:
        if phaseOrNot.get() == 1:
            IWCalc()
        elif phaseOrNot.get() == 2:
            u_fluc = u.copy()
            v_fluc = v.copy()
            u1 = np.mean(u, axis=0)
            v1 = np.mean(v, axis=0)
            u_fluc -= u1
            v_fluc -= v1
            Ff = IntVar(0,45)
            frame = IntVar(0,0)
            fps = IntVar(0,60)
            rpm = IntVar(0,15)
            fps.set(FPSEntry.get())
            rpm.set(TRPMEntry.get())
            Ff.set(ent1t3.get())
            frame.set(ent2t3.get())

            f_omega = (rpm.get()/60)
            input_ang = Ff.get()
            ang = np.cos(np.deg2rad(input_ang))
            filt_freq = 2*f_omega*ang
            L = v_fluc.shape[0]
            freqs = rfftfreq(L)*fps.get()

            vfft_vals = rfft(v_fluc, L, 0)
            ufft_vals = rfft(u_fluc, L, 0)

            trimmed = vfft_vals.copy()
            trimmedU = ufft_vals.copy()

            difference_array = np.abs(freqs-filt_freq)

            closest_index = difference_array.argmin()
            closest_element = freqs[closest_index]
            trimmed[(freqs<closest_element)] = 0
            trimmed[(freqs>closest_element)] = 0
            trimmedU[(freqs<closest_element)] = 0
            trimmedU[(freqs>closest_element)] = 0

            v_postFFT = irfft(trimmed, L, 0)
            u_postFFT = irfft(trimmedU, L, 0)

            UV_postFFT = v_postFFT + u_postFFT

            f.clear()
            ax = f.add_subplot(111)
            a = np.arange(0,UV_postFFT.shape[2],1)
            b = np.arange(0,UV_postFFT.shape[1],1)
            A , B = np.meshgrid(a,b)
            ax.contourf(A,B,UV_postFFT[frame.get(),:,:],locator=ticker.LogLocator(), cmap='seismic')# 40, cmap=)
            ax.xaxis.set_ticks([])
            ax.yaxis.set_ticks([])
            ax.plot()
            plotCanvasFull()
            updateText('Displaying Vertical IW Visualisation')
        else:
            u_fluc = u.copy()
            v_fluc = v.copy()
            u1 = np.mean(u, axis=0)
            v1 = np.mean(v, axis=0)
            u_fluc -= u1
            v_fluc -= v1
            Ff = IntVar(0,45)
            frame = IntVar(0,0)
            fps = IntVar(0,60)
            rpm = IntVar(0,15)   
            fps.set(FPSEntry.get())
            rpm.set(TRPMEntry.get())
            Ff.set(ent1t3.get())
            frame.set(ent2t3.get())  
            f_omega = rpm.get()/60
            input_ang = Ff.get()
            ang = np.cos(np.deg2rad(input_ang))
            filt_freq = 2*f_omega*ang
            L = v_fluc.shape[0]

            cycleL = int(round(fps.get() * (1 / filt_freq)))
            nCycles = math.floor(L / cycleL)

            freqs = rfftfreq(L)*fps.get()
            vfft_vals = rfft(v_fluc, L, 0)
            trimmed = vfft_vals.copy()
            difference_array = np.abs(freqs-filt_freq)
            closest_index = difference_array.argmin()
            closest_element = freqs[closest_index]
            trimmed[(freqs<closest_element)] = 0
            trimmed[(freqs>closest_element)] = 0
            v_postFFT = irfft(trimmed, L, 0)

            for q in range(0, cycleL):
                v_postFFT[q] = np.mean(v_postFFT[q:cycleL*nCycles:cycleL], axis=0)
            v_postFFT = v_postFFT[:cycleL,:,:]

            f.clear()
            ax = f.add_subplot(111)
            a = np.arange(0,v_postFFT.shape[2],1)
            b = np.arange(0,v_postFFT.shape[1],1)
            A , B = np.meshgrid(a,b)
            ax.contourf(A,B,v_postFFT[frame.get(),:,:], 40, cmap='seismic')
            ax.xaxis.set_ticks([])
            ax.yaxis.set_ticks([])
            ax.plot()
            plotCanvasFull()
            freqLabel = Label(tab3, text=("Osciallation period (n. frames): "+ str(cycleL))).grid(row=2, column=3)
            updateText('Displaying Vertical IW Visualisation')
    else:
        pass

def IWCalc():
    if CheckEntries() == 1:
        u_fluc = u.copy()
        v_fluc = v.copy()
        u1 = np.mean(u, axis=0)
        v1 = np.mean(v, axis=0)
        u_fluc -= u1
        v_fluc -= v1
        Ff = IntVar(0,45)
        frame = IntVar(0,0)
        fps = IntVar(0,60)
        rpm = IntVar(0,15)

        fps.set(FPSEntry.get())
        rpm.set(TRPMEntry.get())
        Ff.set(ent1t3.get())
        frame.set(ent2t3.get())

        f_omega = (rpm.get()/60)
        input_ang = Ff.get()
        ang = np.cos(np.deg2rad(input_ang))
        filt_freq = 2*f_omega*ang
        L = v_fluc.shape[0]
        freqs = rfftfreq(L)*fps.get()
        print(freqs)
        vfft_vals = rfft(v_fluc, L, 0)
        trimmed = vfft_vals.copy()
        difference_array = np.abs(freqs-filt_freq)
        closest_index = difference_array.argmin()
        closest_element = freqs[closest_index]
        trimmed[(freqs<closest_element)] = 0
        trimmed[(freqs>closest_element)] = 0
        v_postFFT = irfft(trimmed, L, 0)
        f.clear()
        ax = f.add_subplot(111)
        a = np.arange(0,v_postFFT.shape[2],1)
        b = np.arange(0,v_postFFT.shape[1],1)
        A , B = np.meshgrid(a,b)
        ax.contourf(A,B,v_postFFT[frame.get(),:,:], 40, cmap='seismic')
        ax.xaxis.set_ticks([])
        ax.yaxis.set_ticks([])
        ax.plot()
        plotCanvasFull()
        updateText('Displaying Vertical IW Visualisation')
    else:
        pass

def IWRange():
    if CheckEntries() == 1:
        u_fluc = u.copy()
        v_fluc = v.copy()
        u1 = np.mean(u)
        v1 = np.mean(v)
        u_fluc -= u1
        v_fluc -= v1
        frame = IntVar(0,0)
        fps = IntVar(0,60)
        rpm = IntVar(0,15)

        fps.set(FPSEntry.get())
        rpm.set(TRPMEntry.get())
        frame.set(ent2t3.get())
        f.clear()
        for angle in range(10, 90, 10):
            f_omega = rpm.get()/60
            input_ang = angle
            ang = np.cos(np.deg2rad(input_ang))
            filt_freq = 2*f_omega*ang
            L = v_fluc.shape[0]
            freqs = rfftfreq(L)*fps.get()
            vfft_vals = rfft(v_fluc, L, 0)
            trimmed = vfft_vals.copy()
            difference_array = np.abs(freqs-filt_freq)
            closest_index = difference_array.argmin()
            closest_element = freqs[closest_index]
            trimmed[(freqs<closest_element)] = 0
            trimmed[(freqs>closest_element)] = 0
            v_postFFT = irfft(trimmed, L, 0)
            ax = f.add_subplot(2, 4, angle/10)
            a = np.arange(0,v_postFFT.shape[2],1)
            b = np.arange(0,v_postFFT.shape[1],1)
            A , B = np.meshgrid(a,b)
            ax.contourf(A,B,v_postFFT[frame.get(),:,:], 40, cmap='seismic')
            ax.xaxis.set_ticks([])
            ax.yaxis.set_ticks([])
            ax.plot()
        plotCanvasFull()
        updateText('Displaying Multiple Vertical IW Visualisation')
    else:
        pass

def compData():
    if CheckEntries() == 1:
        u_fluc = u.copy()
        v_fluc = v.copy()
        u1 = np.mean(u, axis=0)
        v1 = np.mean(v, axis=0)
        u_fluc -= u1
        v_fluc -= v1
        fps = IntVar(0,60)
        rpm = IntVar(0,15)   
        fps.set(FPSEntry.get())
        rpm.set(TRPMEntry.get()) 
        f_omega = rpm.get()/60
        vMagArr = []
        for input_ang in range(10, 80):
            ang = np.cos(np.deg2rad(input_ang))
            filt_freq = 2*f_omega*ang
            L = v_fluc.shape[0]
            cycleL = int(round(fps.get() * (1 / filt_freq)))
            nCycles = math.floor(L / cycleL)
            freqs = rfftfreq(L)*fps.get()
            vfft_vals = rfft(v_fluc, L, 0)
            trimmed = vfft_vals.copy()
            difference_array = np.abs(freqs-filt_freq)
            closest_index = difference_array.argmin()
            closest_element = freqs[closest_index]
            trimmed[(freqs<closest_element)] = 0
            trimmed[(freqs>closest_element)] = 0
            v_postFFT = irfft(trimmed, L, 0)
            v_postFFT = abs(v_postFFT)
            for q in range(0, (cycleL-1)):
                v_postFFT[q] = np.mean(v_postFFT[q:cycleL*nCycles:(cycleL-1)], axis=0)
            v_postFFT = v_postFFT[:cycleL,:,:]
            v_postFFTMag = 10* np.mean(v_postFFT)
            vMagArr.append(v_postFFTMag)
        f.clear()
        ax = f.add_subplot(111)
        a = np.arange(10,80,1)
        ax.plot(a,vMagArr)
        ax.set(xlabel='Angle (degrees)', ylabel='Magnitude')
        ax.grid()
        plotCanvasAxes()
        updateText('Displaying Varying Magnitude of IW')
    else:
        pass

phaseOrNot = IntVar()
Radiobutton(tab3, text = "Full Data Set", variable = phaseOrNot, value = 1).grid(row = 0, column = 0)
Radiobutton(tab3, text = "Phase Averaged", variable = phaseOrNot, value = 0).grid(row = 0, column = 1)
Radiobutton(tab3, text = "Bi-directional", variable = phaseOrNot, value = 2).grid(row = 0, column = 3)

label1t3 = Label(tab3, text="Filtering angle: ")
label1t3.grid(row=2, column=0)
ent1t3 = tk.Entry(tab3)
ent1t3.grid(row=3, column=0, columnspan=2)
ent1t3.insert(0, 45)

label2t3 = Label(tab3, text="Frame: ")
label2t3.grid(row=4, column=0)
ent2t3 = tk.Entry(tab3)
ent2t3.grid(row=5, column=0, columnspan=2)
ent2t3.insert(0, 0)

but1t3 = Button(tab3, text='Plot', command=PhaseAv, padx=15)
but1t3.grid(row=6,column=0 )

but2t3 = Button(tab3, text='Plot Range', command=IWRange, padx=15)
but2t3.grid(row=7,column=0 )

but2t3 = Button(tab3, text='Plot Summary', command=compData, padx=15)
but2t3.grid(row=8,column=0 )

############################################################## Function 4 - Inertial wave analysis of frequencies ##########################################

#Step 1 - FFT and band pass filter
def twoPtStep1():
    if CheckEntries() == 1:
        v_fluc = v.copy()
        v1 = np.mean(v, axis=0)
        v_fluc -= v1
        
        Ff = IntVar(0,45)
        frame = IntVar(0,0)
        fps = IntVar(0,60)
        rpm = IntVar(0,15)

        fps.set(FPSEntry.get())
        rpm.set(TRPMEntry.get())
        Ff.set(ent1t3.get())
        frame.set(ent2t3.get())

        f_omega = (rpm.get()/60)
        input_ang = Ff.get()
        ang = np.cos(np.deg2rad(input_ang))
        filt_freq = 2*f_omega*ang
        L = v_fluc.shape[0]
        freqs = rfftfreq(L)*fps.get()
        vfft_vals = rfft(v_fluc, L, 0)
        trimmed = vfft_vals.copy()
        difference_array = np.abs(freqs-filt_freq)
        closest_index = difference_array.argmin()
        closest_element = freqs[closest_index]
        trimmed[(freqs<closest_element)] = 0
        trimmed[(freqs>closest_element)] = 0
        v_postFFT = irfft(trimmed, L, 0)
        print('Step 1 complete')
        twoPtStep2(v, v_postFFT)
    else:
        pass


#Uses unfiltered velocities
def twoPtStepAlt():
    v_fluc = v.copy()
    v1 = np.mean(v, axis=0)
    v_fluc -= v1
    twoPtStep2(v, v_fluc)
    

#Step 2 - Trim into Jet and NoJet
def twoPtStep2(v_input = [[[]]], v_filtered = [[[]]]):
    filterValue = float(ent3t5.get())
    v_trimmed = v_input.copy()
    v_trimmed[v_trimmed > filterValue] = 1
    v_trimmed[v_trimmed < filterValue] = 0
    v_trimmed_average = np.mean(v_trimmed, axis =1)
    v_trimmed_average = np.mean(v_trimmed_average, axis =1)
    v_trimmed_average_smoothed = []
    A = 30
    for i in range(math.floor(len(v_trimmed_average)/A)):
        v_trimmed_average_smoothed_mag = np.mean(v_trimmed_average[A*(i):A*(i+1)])
        v_trimmed_average_smoothed.append(v_trimmed_average_smoothed_mag)

    filterValue2 = max(v_trimmed_average_smoothed)/20
    Block = np.array(v_trimmed_average_smoothed.copy())
    Block[Block > filterValue2] = 1
    Block[Block < filterValue2] = 0
    

    for j in range(1,(len(Block)-1)):
        if Block[j] != Block[j-1] and Block[j] != Block[j+1]:
            Block[j] = Block[j+1]
        else:
            pass

    jetV = np.empty((1, v_input.shape[1], v_input.shape[2]))
    noJetV = np.empty((1, v_input[0].shape[0], v_input[0].shape[1]))

    for k in range(v_filtered.shape[0]-A):
        if Block[math.floor(k/A)] == 1:
            jetV = np.concatenate((jetV, np.transpose(np.atleast_3d(v_filtered[k,:,:]), (2, 0, 1))))
        else:
            noJetV = np.concatenate((noJetV, np.transpose(np.atleast_3d(v_filtered[k,:,:]), (2, 0, 1))))   
    jetV = jetV[1:,:,:]
    noJetV = noJetV[1:,:,:]
    
    print('Step 2 complete')
    corr_Jet_Hor, dist_Jet_Hor, corr_noJet_Hor, dist_noJet_Hor = twoPtStep3(jetV, noJetV)
    print('Step 3 complete')
    corr_Jet_Vert, dist_Jet_Vert, corr_noJet_Vert, dist_noJet_Vert = twoPtStep4(jetV, noJetV)
    print('Step 4 complete')
    DistCorrJetVert,DistCorrNoJetVert = twoPtStep5(corr_Jet_Vert, dist_Jet_Vert, corr_noJet_Vert, dist_noJet_Vert)
    DistCorrJetHor,DistCorrNoJetHor = twoPtStep5(corr_Jet_Hor, dist_Jet_Hor, corr_noJet_Hor, dist_noJet_Hor)
    print('Step 5 complete')
    twoPtStep6(DistCorrJetVert,DistCorrNoJetVert,DistCorrJetHor,DistCorrNoJetHor)


#Step 3 - Two pt Corr Horizontallly
def twoPtStep3(v_jet_in = [[[]]], v_nojet_in = [[[]]]):
    print(str(v_jet_in.shape) + '  -  ' + str(v_nojet_in.shape))

    corr_Jet_Hor = []
    dist_Jet_Hor = []
    
    corr_noJet_Hor = []
    dist_noJet_Hor = []

    for i in range(0, v_jet_in.shape[1]):
        for j in range(0, v_jet_in.shape[2]):
            corr_temp = np.dot(v_jet_in[:,i,j], v_jet_in[:,i,j])
            dist_temp = 0
            corr_Jet_Hor.append(corr_temp)
            dist_Jet_Hor.append(dist_temp)

    for i in range(0, v_jet_in.shape[1]):
        for pair in itertools.combinations(range(len(v_jet_in[1,i,:])), 2):
            corr_temp = np.dot(v_jet_in[:,i,pair[0]], v_jet_in[:,i,pair[1]])
            dist_temp = abs(pair[0] - pair[1])
            corr_Jet_Hor.append(corr_temp)
            dist_Jet_Hor.append(dist_temp)
            
    for i in range(0, v_nojet_in.shape[1]):
        for j in range(0, v_nojet_in.shape[2]):
            corr_temp = np.dot(v_nojet_in[:,i,j], v_nojet_in[:,i,j])
            dist_temp = 0
            corr_noJet_Hor.append(corr_temp)
            dist_noJet_Hor.append(dist_temp)

    for i in range(0, v_nojet_in.shape[1]):
        for pair in itertools.combinations(range(len(v_nojet_in[1,i,:])), 2):
            corr_temp = np.dot(v_nojet_in[:,i,pair[0]], v_nojet_in[:,i,pair[1]])
            dist_temp = abs(pair[0] - pair[1])
            corr_noJet_Hor.append(corr_temp)
            dist_noJet_Hor.append(dist_temp) 

    return corr_Jet_Hor, dist_Jet_Hor, corr_noJet_Hor, dist_noJet_Hor


#Step 4 - Two pt Corr Vertically
def twoPtStep4(v_jet_in = [[[]]], v_nojet_in = [[[]]]):

    corr_Jet_Vert = []
    dist_Jet_Vert = []
    
    corr_noJet_Vert = []
    dist_noJet_Vert = []
    
    for j in range(0, v_jet_in.shape[2]):
        for i in range(0, v_jet_in.shape[1]):
            corr_temp = np.dot(v_jet_in[:,i,j], v_jet_in[:,i,j])
            dist_temp = 0
            corr_Jet_Vert.append(corr_temp)
            dist_Jet_Vert.append(dist_temp)   

    for j in range(0, v_jet_in.shape[2]):
        for pair in itertools.combinations(range(len(v_jet_in[1,:,j])), 2):
            corr_temp = np.dot(v_jet_in[:,pair[0],j], v_jet_in[:,pair[1],j])
            dist_temp = abs(pair[0] - pair[1])
            corr_Jet_Vert.append(corr_temp)
            dist_Jet_Vert.append(dist_temp)   

    for j in range(0, v_nojet_in.shape[2]):
        for i in range(0, v_nojet_in.shape[1]):
            corr_temp = np.dot(v_nojet_in[:,i,j], v_nojet_in[:,i,j])
            dist_temp = 0
            corr_noJet_Vert.append(corr_temp)
            dist_noJet_Vert.append(dist_temp)   
  
    for j in range(0, v_nojet_in.shape[2]):
        for pair in itertools.combinations(range(len(v_nojet_in[1,:,j])), 2):
            corr_temp = np.dot(v_nojet_in[:,pair[0],j], v_nojet_in[:,pair[1],j])
            dist_temp = abs(pair[0] - pair[1])
            corr_noJet_Vert.append(corr_temp)
            dist_noJet_Vert.append(dist_temp)   
    
    return corr_Jet_Vert, dist_Jet_Vert, corr_noJet_Vert, dist_noJet_Vert


#Step 5 - Gathering like distancces
def twoPtStep5(corr_Jet, dist_Jet, corr_noJet, dist_noJet):
    DistCorrJet = np.asarray(f_dict(dist_Jet, corr_Jet))
    DistCorrNoJet = np.asarray(f_dict(dist_noJet, corr_noJet))

    DistCorrJet[1,:] = DistCorrJet[1,:]/DistCorrJet[1,0]
    DistCorrNoJet[1,:] = DistCorrNoJet[1,:]/DistCorrNoJet[1,0] 

    return DistCorrJet, DistCorrNoJet


#Step 6 - Gather angle using Hor/Vert relation and plot
def twoPtStep6(var1, var2, var3, var4):

    f1 = interp1d(var1[0], var1[1], kind='cubic')
    print(f1)

    f.clear()
    ax1 = f.add_subplot(2, 1, 1)
    ax1.plot(var1[0], var1[1], 'xb', label = 'Jet')    
    ax1.plot(var2[0], var2[1], 'xr', label = 'Suppressed')  
    ax1.legend(loc="upper right")
    ax1.set(xlabel='Distance between Points', ylabel='Magnitude of Correlation (Vertical)')
    ax2 = f.add_subplot(2, 1, 2)
    ax2.plot(var3[0], var3[1], 'xb', label = 'Jet')    
    ax2.plot(var4[0], var4[1], 'xr', label = 'Suppressed')  
    ax2.legend(loc="upper right")
    ax2.set(xlabel='Distance between Points', ylabel='Magnitude of Correlation (Horizontal)')
    plotCanvasAxes()
    updateText('Displaying Total 2Pt Corr Data')


but1t4 = Button(tab4, text='Two Point Begin', command=twoPtStep1, padx=15)
but1t4.grid(row=5,column=0)

but2t4 = Button(tab4, text='Two Point Begin (Alt)', command=twoPtStepAlt, padx=15)
but2t4.grid(row=6,column=0)


############################################################## Function 5 - Single zone motion tracking ##########################################



def plotCoord():
    u1 = np.mean(u, axis=0)
    v1 = np.mean(v, axis=0)
    a = np.arange(0,u.shape[2],1)
    b = np.arange(0,u.shape[1],1)
    mag = np.sqrt(u1**2 + v1**2)
    A , B = np.meshgrid(a,b)
    f.clear()
    c = IntVar(0,41)
    d = IntVar(0,32)
    c.set(ent1t5.get())
    d.set(ent2t5.get())
    quiv = f.add_subplot(111)
    quiv.quiver(A,B,u1,v1,mag)
    quiv.xaxis.set_ticks([])
    quiv.yaxis.set_ticks([])
    quiv.plot()
    quiv.plot(c.get(),d.get(),'ro') 
    plotCanvasFull()
    updateText('Co-ordinates overlaid on mean velocity')

def ZoneTracking():
    v_single = []
    c = IntVar(0,41)
    d = IntVar(0,32)
    c.set(ent2t5.get())
    d.set(ent1t5.get())
    v_copy = np.array(v.copy())
    if selectedParticles.get() == 0:
        v_single = v_copy[:,c.get(),d.get()]
        f.clear()
        hist = f.add_subplot(111)
        hist.hist(v_single, bins=50, rwidth=0.8,log=True)
        #hist.plot()
        hist.grid(True)
        #plt.yscale('log', nonposy='clip')
        plt.plot()
        plotCanvasAxes()
        updateText('Displaying PDF-ish for given co-ords')
    elif selectedParticles.get() == 1:
        v_single1 = v_copy[:,c.get(),d.get()]
        v_single2 = v_copy[:,c.get()-1,d.get()-1]
        v_single3 = v_copy[:,c.get()-1,d.get()+1]
        v_single4 = v_copy[:,c.get()+1,d.get()-1]
        v_single5 = v_copy[:,c.get()+1,d.get()+1]
        v_single = np.concatenate((v_single1, v_single2, v_single3, v_single4, v_single5))
        f.clear()
        hist = f.add_subplot(111)
        hist.hist(v_single, bins=50, rwidth=0.8,log=True)
        hist.grid(True)
        plt.plot()
        plotCanvasAxes()
        updateText('Displaying PDF-ish for given co-ords')
    else:
        v_single1 = v_copy[:,c.get(),d.get()]
        v_single2 = v_copy[:,c.get()-1,d.get()-1]
        v_single3 = v_copy[:,c.get()-1,d.get()+1]
        v_single4 = v_copy[:,c.get()+1,d.get()-1]
        v_single5 = v_copy[:,c.get()+1,d.get()+1]
        v_single6 = v_copy[:,c.get()-2,d.get()-2]
        v_single7 = v_copy[:,c.get()-2,d.get()+2]
        v_single8 = v_copy[:,c.get()+2,d.get()-2]
        v_single9 = v_copy[:,c.get()+2,d.get()+2]
        v_single = np.concatenate((v_single1, v_single2, v_single3, v_single4, v_single5, v_single6, v_single7, v_single8, v_single9))
        f.clear()
        hist = f.add_subplot(111)
        hist.hist(v_single, bins=50, rwidth=0.8,log=True)
        hist.grid(True)
        plt.plot()
        plotCanvasAxes()
        updateText('Displaying PDF-ish for given co-ords')

def trimVelocities():
    if smoothOrNot.get() == 0:
        filterValue = float(ent3t5.get())
        v_trimmed = v.copy()
        v_trimmed[v_trimmed < filterValue] = 0        
        v_trimmed[v_trimmed > filterValue] = 1

        v_trimmed_average = np.mean(v_trimmed, axis =1)
        v_trimmed_average = np.mean(v_trimmed_average, axis =1)
        
        f.clear()
        ax = f.add_subplot(111)
        a = np.arange(0,v.shape[0],1)
        ax.plot(a,v_trimmed_average)
        ax.set(xlabel='Frame', ylabel='Magnitude')
        ax.grid()
        plotCanvasAxes()
        updateText('Displaying number of jet u values')
    if smoothOrNot.get() == 1:
        filterValue = float(ent3t5.get())
        v_trimmed = v.copy()
        v_trimmed[v_trimmed < filterValue] = 0
        v_trimmed[v_trimmed > filterValue] = 1

        v_trimmed_average = np.mean(v_trimmed, axis =1)
        v_trimmed_average = np.mean(v_trimmed_average, axis =1)
        v_trimmed_average_smoothed = []
        A = 50
        for i in range(math.floor(len(v_trimmed_average)/A)):
            v_trimmed_average_smoothed_mag = np.mean(v_trimmed_average[A*(i):A*(i+1)])
            v_trimmed_average_smoothed.append(v_trimmed_average_smoothed_mag)
        f.clear()
        ax = f.add_subplot(111)
        a = np.arange(1, len(v_trimmed_average_smoothed)*5 ,5)
        ax.plot(a,v_trimmed_average_smoothed)
        ax.set(xlabel='Frame', ylabel='Magnitude')
        ax.grid()
        plotCanvasAxes()
        updateText('Displaying number of jet u values')

def TrimAndFFT():
    filterValue = float(ent3t5.get())
    v_trimmed = v.copy()
    v_trimmed[v_trimmed < filterValue] = 0    
    v_trimmed[v_trimmed > filterValue] = 1

    v_trimmed_average = np.mean(v_trimmed, axis =1)
    v_trimmed_average = np.mean(v_trimmed_average, axis =1)
    fps = IntVar(0,60)
    fps.set(FPSEntry.get())
    L = len(v_trimmed_average)
    freqs = rfftfreq(L)*fps.get()
    vfft_vals = rfft(v_trimmed_average, L) 
    f.clear()
    ax1 = f.add_subplot(2, 1, 1)
    a = np.arange(0,v.shape[0],1)
    ax1.plot(a,v_trimmed_average)
    ax1.set(xlabel='Frame', ylabel='Magnitude')
    ax1.grid()
    ax2 = f.add_subplot(2, 1, 2)
    ax2.plot(freqs,vfft_vals)
    plotCanvasAxes()
    updateText('Displaying FFT of F.B cycle')

def PlotTrimandFilter():
    filterValue = float(ent3t5.get())
    v_trimmed = v.copy()
    v_trimmed[v_trimmed < filterValue] = 0    
    v_trimmed[v_trimmed > filterValue] = 1

    v_trimmed_average = np.mean(v_trimmed, axis =1)
    v_trimmed_average = np.mean(v_trimmed_average, axis =1)
    v_trimmed_average_smoothed = []
    A = 30
    for i in range(math.floor(len(v_trimmed_average)/A)):
        v_trimmed_average_smoothed_mag = np.mean(v_trimmed_average[A*(i):A*(i+1)])
        v_trimmed_average_smoothed.append(v_trimmed_average_smoothed_mag)
    f.clear()
    ax1 = f.add_subplot(2, 1, 1)
    a = np.arange(1, len(v_trimmed_average_smoothed)*A ,A)
    ax1.plot(a,v_trimmed_average_smoothed)
    ax1.set(xlabel='Frame', ylabel='Magnitude')
    ax1.grid()

    filterValue2 = max(v_trimmed_average_smoothed)/20
    Block = np.array(v_trimmed_average_smoothed.copy())
    Block[Block > filterValue2] = 1
    Block[Block < filterValue2] = 0
    
    for j in range(2,len(Block)-1):
        if Block[j] != Block[j-1] and Block[j] != Block[j+1]:
            Block[j] = Block[j+1]
        else:
            pass

    ax2 = f.add_subplot(2, 1, 2)
    ax2.plot(a, Block)
    plotCanvasAxes()
    updateText('Displaying number of jet u values')


selectedParticles = IntVar()
Label(tab5, text=" ", padx=25).grid(row=0, column=5)

Radiobutton(tab5, text = "1 Particle", variable = selectedParticles, value = 0).grid(row = 4, column = 6)
Radiobutton(tab5, text = "5 Particles", variable = selectedParticles, value = 1).grid(row = 5, column = 6)
Radiobutton(tab5, text = "9 Particles", variable = selectedParticles, value = 2).grid(row = 6, column = 6)

but1t5 = Button(tab5, text='Plot Average', command=AverageCalc,  padx=15)
but1t5.grid(row=1,column=3 )
but2t5 = Button(tab5, text='Plot Co-ord', command=plotCoord,  padx=15)
but2t5.grid(row=1,column=4 )
but3t5 = Button(tab5, text='Plot Trim', command=PlotTrimandFilter,  padx=15)
but3t5.grid(row=1,column=5 )

label1t5 = Label(tab5, text="x co-ord:")
label1t5.grid(row=2, column=1)
ent1t5 = tk.Entry(tab5)
ent1t5.grid(row=3, column=1, columnspan=2)
ent1t5.insert(0, 41)

label2t5 = Label(tab5, text="y co-ord:")
label2t5.grid(row=4, column=1)
ent2t5 = tk.Entry(tab5)
ent2t5.grid(row=5, column=1, columnspan=2)
ent2t5.insert(0, 32)

but3t5 = Button(tab5, text='Plot Graph', command=ZoneTracking,  padx=15)
but3t5.grid(row=6,column=1 )

Label(tab5, text=" ", pady=10).grid(row=7, column=1)
label3t5 = Label(tab5, text="x co-ord:")
label3t5.grid(row=8, column=1)
ent3t5 = tk.Entry(tab5)
ent3t5.grid(row=9, column=1, columnspan=2)
ent3t5.insert(0, 1)

but4t5 = Button(tab5, text='Plot Analysis', command=trimVelocities,  padx=15)
but4t5.grid(row=10,column=1 )
but4t5 = Button(tab5, text='Overlay FFT', command=TrimAndFFT,  padx=15)
but4t5.grid(row=11,column=1 )

smoothOrNot = IntVar()

Radiobutton(tab5, text = "Raw Data", variable = smoothOrNot, value = 0).grid(row = 9, column = 6)
Radiobutton(tab5, text = "Smoothed", variable = smoothOrNot, value = 1).grid(row = 10, column = 6)

root.mainloop()