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
from mpl_toolkits import mplot3d

#Define global variables 
u = [[[]]]
v = [[[]]]
u_temp = [[[]]]
v_temp = [[[]]]

#Create main GIU window
root = Tk()
directory = filedialog.askopenfilename()


file_ext = os.path.splitext(directory)
if os.path.exists(directory) == FALSE:
    print("That file does not exist")
elif file_ext[1] != ".mat":
    print("Please choose a .mat data file")
else:
    os.chdir(os.path.dirname(directory))
    mat_contents = io.loadmat(os.path.basename(directory))
    u_temp = np.squeeze(mat_contents['u_filtered']) 
    v_temp = np.squeeze(mat_contents['v_filtered'])
    print("Filtered Data Imported")

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


def twoPointCorr():
    a = np.arange(0,u.shape[2]*u.shape[1],1)
    out = np.array(np.meshgrid(a,a)).T.reshape(-1,2)
    print(out.shape)    
    print(out)
    for P1 in range(0, out.shape):
        2 
    u_long = u.copy().reshape((u.shape[2]*u.shape[1],u.shape[0]))
    print(u_long.shape)

twoPointCorr()

