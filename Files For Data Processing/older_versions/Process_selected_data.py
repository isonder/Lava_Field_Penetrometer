# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 17:09:28 2024
Last modified on Mar 4 10:48 2024

@author: Marti
"""

import numpy as np

import pandas as pd



from tkinter import Tk
from tkinter.filedialog import askdirectory
Folder = askdirectory(title='Select Folder') # shows dialog box and return the path
Wd = (Folder)  


import os
os.chdir(Wd)
# import os
# os.chdir(r'C:\Users\Marti\Desktop\Academic Work\UB\UB_PhD_2022\Models\Py_spy\Field Rheometer data')
import pandas as pd
import math 
import matplotlib.pyplot as plt
import statistics
from scipy.stats import sem
from scipy import stats
import statsmodels.api as sm
import numpy as np
import easygui
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QtCore, QtGui
# from PyQt6.QtCore import Qt
# from PyQt6 import uic
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import math 
pi_3= 3*(math.pi)
pi_6= 6*(math.pi)

path = easygui.fileopenbox()
# path2 = easygui.fileopenbox()
# p= path[113:135]
#p= path[-27:]
p= path[-16:]

#####use this code to rewrite text file with commmas before, then clear variables and reload the files###
# with open(p, "r") as f:
#     data = f.read().replace(" ", ",")
# x= data

# #open text file
# text_file = open(path, "w")
 
# #write string to file
# n = text_file.write(x)
 
# #close file
# text_file.close()
# #p= path
#########################################################
df= pd.read_csv(p, delim_whitespace=True)
#df.columns = ['Time(s)', 'Distance_mm','Force(N)','Temperature(C)']# specifiy which columns you want, here i have removed date
df.columns = ['Time(s)', 'Distance_mm','Force(N)']
filename= p[:18]
#fig,axa1=plt.subplots(figsize=(8, 6))
# fig = plt.figure(figsize=(10, 7))

#fig,axa1 = plt.subplots(figsize=(8, 6))
# axa1 = fig.add_subplot(211)

t = df['Time(s)'] 
#T = df['Temperature(C)']
F = df['Force(N)']
D = df['Distance_mm']
Dmet = D/1000
D= Dmet
t=t.to_numpy()#this is needed for the derivative later

import warnings
def moving_average(data, window_size):
    """
    Calculates the moving average of a 1-dimensional array using a specified
    window size. The window is centered around each index, and decreases at
    the ends of the input array.

    Parameters
    ----------
    data : The input 1-dimensional array.
    window_size : int
        The window size. This should be an odd number. If it is even it will
        be increased by 1 to have a symmetric window around each element.
    """
    if window_size % 2 == 0:
        warnings.warn(f"Got an even sized {window_size=}. Increasing it by 1")
        window_size += 1
    wh = window_size // 2  # Half window: Number of samples before/after current
    result = np.empty_like(data)  # Return values as a numpy array, not a list
    length = len(data)
    for i in range(length):
        if i < wh:  # Average over smaller interval at beginning
            result[i] = sum(data[:2 * i + 1]) / (2 * i + 1)
        elif length - i <= wh:    # Average over smaller interval at end
            l = 2 * i - length + 1
            # print(f"{i=},  {l=}")
            result[i] = sum(data[l:]) / (length - l)
        else:
            result[i] = sum(data[i - wh:i + wh + 1]) / window_size
    return result


#window_size=len(df)
window_size=5

Favg = moving_average(F, window_size)
Davg = moving_average(D, window_size)
tavg = moving_average(t, window_size)


############ Here we calculate the velocity as a derivative of displacement and time######
def derivative_central(y, t):
    """
    Computes dy/dt based on central difference.

    Parameters:
    y : array-like
        The dependent variable.
    t : array-like
        The independent variable.

    Returns:
    der : array-like
        The derivative of y with respect to t.
    """
    der = np.empty_like(y)
    der[1:-1] = (y[2:] - y[:-2]) / (t[2:] - t[:-2])
    # Assume same derivative value for first and last element as the
    # second, second last element, respectively
    der[[0, -1]] = der[[1, -2]]
    return der


vel = -derivative_central(Davg,t )
print(vel)

####################################################

#################Here we apply the calibration factors based on three ranges###################

FOV_LOW = 2.0e3
FOV_HIGH = 1.5e4

# Calibration as listed in Table 1
cal = {
    'low': {'m': 1.736, 'b': -432.49},
    'med': {'m': 2.7504, 'b': -223.8},
    'high': {'m': 1.8734, 'b': 3.3905e4}
}


def eta(force, vel):
    """Calculated viscosity from above calibration values.
    Parameters
    ----------
    force
    vel
    """
    visc = np.empty_like(force)
    fov = force / vel
    idx = fov < FOV_LOW
    if np.any(idx):
        calib = cal['low']
        visc[idx] = calib['m'] * fov[idx] + calib['b']
    idx = np.logical_and(fov >= FOV_LOW, fov <= FOV_HIGH)
    if np.any(idx):
        calib = cal['med']
        visc[idx] = calib['m'] * fov[idx] + calib['b']
    idx = fov > FOV_HIGH
    if np.any(idx):
        calib = cal['low']
        visc[idx] = calib['m'] * fov[idx] + calib['b']
    return visc


cal_visc= eta(Favg, vel) #####this is now the raw calibrated viscosity 

############################


Lengthcal2 = len(cal_visc)
print(Lengthcal2)

Vmavgcal2 =moving_average(cal_visc, window_size)#########we smooth the calibrated viscosity here

Length_2cal2 = len(cal_visc)
print(Length_2cal2)


#########this determines the depth of penetration#############
x2cal2= list(range(0,Length_2cal2))
print(x2cal2)
Dstart2=D[0]
print(Dstart2)
Dend2=D.iloc[-1]
dis_tot2 = (Dstart2-Dend2)#/1000
print(dis_tot2)
z2= len(x2cal2)
print(z2)
zz2= dis_tot2/z2
print(zz2)

    
xz2= np.linspace(0,dis_tot2,z2)


###########final plots############
plt.plot(x2cal2, Vmavgcal2, 'o-', color ='green', markerfacecolor = 'none', markeredgecolor = 'k' , label= 'vcal_smooth')
#plt.plot(xcal, Vconfcal, 'o-', color ='red', markerfacecolor = 'none', markeredgecolor = 'r' , label= 'vcal_raw')
#plt.plot(x2, Vmavg, 'o-', color ='green', markerfacecolor = 'none', markeredgecolor = 'g' , label= 'Viscosity_smooth')
#plt.plot(x, Vconf, 'o-', color ='blue', markerfacecolor = 'none', markeredgecolor = 'b' , label= 'Viscosity_raw')
plt.legend(loc="upper left")
plt.ylabel('Viscosity Pas')
plt.xlabel('data (n)')
  #label="Viscosity vs time ")

plt.show()

#plt.plot(x2cal, Vmavgcal, 'o-', color ='black', markerfacecolor = 'none', markeredgecolor = 'k' , label= 'vcal_smooth')
plt.plot(x2cal2, cal_visc, 'o-', color ='orange', markerfacecolor = 'none', markeredgecolor = 'r' , label= 'vcal_raw')
#plt.plot(x2, Vmavg, 'o-', color ='green', markerfacecolor = 'none', markeredgecolor = 'g' , label= 'Viscosity_smooth')
#plt.plot(x, Vconf, 'o-', color ='blue', markerfacecolor = 'none', markeredgecolor = 'b' , label= 'Viscosity_raw')
plt.legend(loc="upper left")
plt.ylabel('Viscosity Pas')
plt.xlabel('data (n)')


plt.show()


plt.plot(xz2, Vmavgcal2, 'o-', color ='blue', markerfacecolor = 'none', markeredgecolor = 'k' , label= 'vcal_to_distance')
plt.legend(loc="upper left")
plt.ylabel('Viscosity Pas')
plt.xlabel('lenght (m)')
plt.show()



###export data into .txt files 
np.savetxt("exported_cal_dat.txt", np.c_[x2cal2, Vmavgcal2, xz2])



