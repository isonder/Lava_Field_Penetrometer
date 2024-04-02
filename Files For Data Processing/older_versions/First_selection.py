
from tkinter import Tk
from tkinter.filedialog import askdirectory
Folder = askdirectory(title='Select Folder') # shows dialog box and return the path
Wd = (Folder)  


import os
os.chdir(Wd)

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

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import math 
pi_3= 3*(math.pi)
pi_6= 6*(math.pi)

path = easygui.fileopenbox()

p= path[-27:]


columns = ['Time(s)', 'Force(N)', 'Distance_mm']# specifiy which columns you want, here i have removed date
df= pd.read_csv(p, usecols=columns, delim_whitespace=True)

filename= p[:18]




t = df['Time(s)'] 
F = df['Force(N)']
D = df['Distance_mm']

fig = plt.figure(figsize=(10, 7))


axa1 = fig.add_subplot(211)


t = t.values
D = D.values
F = F.values



p1, = axa1.plot(t, F, 'r-')


axa1.set_title('Press left mouse button and drag to test')
axa1.set_xlabel('time (s)', color='black')
axa1.set_ylabel('Force (N)', color='red')

axa1.tick_params(axis='y', color='red', labelcolor= 'red')


axa2 = axa1.twinx()
axa2.plot(t, D, 'g-')
axa2.set_ylabel('Distance (mm)', color='green')
axa2.grid(False)
axa2.set_xlabel('time (s)', color='black')
axa2.tick_params(axis='y', color='green', labelcolor= 'green')
axa2.spines.left.set_position(("axes", 1.08))




axb = fig.add_subplot(212)
axb.set_xlabel('time (s)', color='black')
axb.set_ylabel('Force (N)', color='red')
axb1 = axb.twinx()
axb1.set_ylabel('Distance (mm)', color='green')
axb1.grid(False)
axb1.set_xlabel('time (s)', color='black')
axb1.tick_params(axis='y', color='green', labelcolor= 'green')
axb1.spines.left.set_position(("axes", 1.08))

line2, = axb.plot(t, F, 'r-')
line2b, = axb1.plot(t, D, 'g-')


def onselect(tmin, tmax):
    indmin, indmax = np.searchsorted(t, (tmin, tmax))
    indmax = min(len(t) - 1, indmax)

    thist = t[indmin:indmax]
    thisD = D[indmin:indmax]
    thisF = F[indmin:indmax]

    line2.set_data(thist, thisF)
    line2b.set_data(thist, thisD)

    axb.set_xlim(thist[0], thist[-1])
    axb.set_ylim(thisF.min(), thisF.max())
    axb1.set_xlim(thist[0], thist[-1])
    axb1.set_ylim(thisD.min(), thisD.max())

    fig.canvas.draw_idle()

    
    np.savetxt("selected_dat.txt", np.c_[thist, thisD, thisF])



span = SpanSelector(axa2, onselect, 'horizontal', useblit=True,
                    rectprops=dict(alpha=0.5, facecolor='red'))

plt.subplots_adjust(left=0.125, bottom=0.135, right=0.845, top=0.905, wspace=None, hspace=None)
plt.show()


