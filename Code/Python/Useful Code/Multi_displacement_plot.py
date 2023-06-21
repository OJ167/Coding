import matplotlib.pyplot as plt
import numpy as np

import os
import sys

dirPath = os.getcwd()
sys.path.insert(0, dirPath)
import OllieTools as oj

# data = np.load("F:\Experiments\FlowVis\Dye Videos\Ring_Tracking_Results\Variables/Vars.npz")
data = np.load('/Volumes/OllieSSD/Experiments/FlowVis/Dye Videos/Ring_Tracking_Results/Variables/Vars.npz')
# data = np.load('/Volumes/OllieSSD/Experiments/FlowVis/Dye Videos/Repeatability/Ring Tracking Data/Variables/0RPM.npz')

Ring1_0 = np.asarray(data["Ring1_0"])
# Ring2_0 = np.asarray(data["Ring2_0"])
# Ring3_0 = np.asarray(data["Ring3_0"])
Ring1_27 = np.asarray(data["Ring1_27"])
# Ring2_27 = np.asarray(data["Ring2_27"])
# Ring3_27 = np.asarray(data["Ring3_27"])
# Ring1_6 = np.asarray(data["Ring1_6"])
Ring2_6 = np.asarray(data["Ring2_6"])
# Ring3_6 = np.asarray(data["Ring3_6"])
# Ring4_6 = np.asarray(data["Ring4_6"])
# Ring1_87 = np.asarray(data["Ring1_87"])
# Ring2_87 = np.asarray(data["Ring2_87"])
Ring3_87 = np.asarray(data["Ring3_87"])

plt.style.reload_library()
plt.style.use('science')

plt.plot(Ring1_0[1,1:264]/95  ,  label = "0.0RPM")
# plt.plot(Ring2_0[1,1:]  ,  label = "Ring2_0")
# plt.plot(Ring3_0[1,1:]  ,  label = "Ring3_0")
plt.plot(Ring1_27[1,1:275]/95 ,  label = "2.7RPM")
# plt.plot(Ring2_27[1,1:] ,  label = "Ring2_27")
# plt.plot(Ring3_27[1,1:] ,  label = "Ring3_27")
# plt.plot(Ring1_6[1,1:]  ,  label = "Ring1_6")
plt.plot(Ring2_6[1,1:]/95  ,  label = "6.0RPM")
# plt.plot(Ring3_6[1,1:]  ,  label = "Ring3_6")
# plt.plot(Ring4_6[1,1:]  ,  label = "Ring4_6")
# plt.plot(Ring1_87[1,1:] ,  label = "Ring1_87")
# plt.plot(Ring2_87[1,1:] ,  label = "Ring2_87")
plt.plot(Ring3_87[1,1:]/95 ,  label = "8.7RPM")

# Ring1_0[1,1:]  ,
# Ring2_0[1,1:]  ,
# Ring3_0[1,1:]  ,
# Ring1_27[1,1:] ,
# Ring2_27[1,1:] ,
# Ring3_27[1,1:] ,
# Ring1_6[1,1:]  ,
# Ring2_6[1,1:]  ,
# Ring3_6[1,1:]  ,
# Ring4_6[1,1:]  ,
# Ring1_87[1,1:] ,
# Ring2_87[1,1:] ,
# Ring3_87[1,1:] ,

# Ring1_0  = np.asarray(data["Ring1_0"])
# Ring2_0  = np.asarray(data["Ring2_0"])
# Ring3_0  = np.asarray(data["Ring3_0"])
# Ring4_0  = np.asarray(data["Ring4_0"])
# Ring5_0  = np.asarray(data["Ring5_0"])
# Ring6_0  = np.asarray(data["Ring6_0"])
# Ring7_0  = np.asarray(data["Ring7_0"])
# Ring8_0  = np.asarray(data["Ring8_0"])
# Ring9_0  = np.asarray(data["Ring9_0"])
# Ring10_0 = np.asarray(data["Ring10_0"])


# plt.plot(Ring1_0[1,1:]/95  ,  label = "Ring1 0.0RPM")
# plt.plot(Ring2_0[1,1:]/95  ,  label = "Ring2 0.0RPM") #bad
# plt.plot(Ring3_0[1,1:]/95  ,  label = "Ring2 0.0RPM")
# plt.plot(Ring4_0[1,1:]/95  ,  label = "Ring3 0.0RPM")
# plt.plot(Ring5_0[1,1:]/95  ,  label = "Ring4 0.0RPM")
# plt.plot(Ring6_0[1,1:]/95  ,  label = "Ring5 0.0RPM")
# plt.plot(Ring7_0[1,1:]/95  ,  label = "Ring6 0.0RPM")
# plt.plot(Ring8_0[1,1:]/95  ,  label = "Ring8 0.0RPM") #bad
# plt.plot(Ring9_0[1,1:]/95  ,  label = "Ring7 0.0RPM")
# plt.plot(Ring10_0[1,1:]/95  ,  label = "Ring8 0.0RPM")


# plt.xlabel('Time [Frames]')
# plt.xticks(Ring1_0[:,2]/100)
plt.xlabel('[T/(Dp/Up)]')
plt.ylabel('[Z/Dp]')
plt.title("Multiple Ring Displacement")

plt.legend()
plt.show()
