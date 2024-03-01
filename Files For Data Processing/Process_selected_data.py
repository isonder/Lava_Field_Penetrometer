# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 17:09:28 2024
Last modified on Mar 1 10:18 2024

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


def moving_average(data, window_size):
    """
    Calculates the moving average of a 1-dimensional array using a specified window size.

    Args:
    - data: The input 1-dimensional array.
    - window_size: The size of the window for the moving average.

    Returns:
    - result: The array containing the moving averages.
    """
    result = []
    for i in range(len(data)):
        if i < window_size - 1:
            result.append(sum(data[:i + 1]) / (i + 1))
        else:
            result.append(sum(data[i - window_size + 1:i + 1]) / window_size)
    return result


#window_size=len(df)
window_size=4

Favg = moving_average(F, window_size)
Davg = moving_average(D, window_size)
tavg = moving_average(t, window_size)



plt.plot(t, F, 'o-', color ='black', markerfacecolor = 'none', markeredgecolor = 'k' , label= 'force')
#plt.plot(xcal, Vconfcal, 'o-', color ='red', markerfacecolor = 'none', markeredgecolor = 'r' , label= 'vcal_raw')
plt.plot(t, Favg, 'o-', color ='green', markerfacecolor = 'none', markeredgecolor = 'g' , label= 'favg')
plt.legend(loc="upper left")
plt.ylabel('force')
plt.xlabel('time')
  #label="Viscosity vs time ")
plt.show()

plt.plot(t, D, 'o-', color ='blue', markerfacecolor = 'none', markeredgecolor = 'b' , label= 'distance')
#plt.plot(xcal, Vconfcal, 'o-', color ='red', markerfacecolor = 'none', markeredgecolor = 'r' , label= 'vcal_raw')
plt.plot(t, Davg, 'o-', color ='purple', markerfacecolor = 'none', markeredgecolor = 'm' , label= 'davg')


plt.legend(loc="upper left")
plt.ylabel('displacement')
plt.xlabel('time')
  #label="Viscosity vs time ")
plt.show()

plt.plot(t, tavg, 'o-', color ='purple', markerfacecolor = 'none', markeredgecolor = 'm' , label= 'davg')


plt.legend(loc="upper left")
plt.ylabel('tavg')
plt.xlabel('time')
  #label="Viscosity vs time ")
plt.show()






fig = plt.figure(figsize=(10, 7))

#fig,axa1 = plt.subplots(figsize=(8, 6))
axa1 = fig.add_subplot(211)

p1, = axa1.plot(t, F, 'r-')

#axa1.set_ylim(0, 400)
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
axb.set_ylabel('Force (N)', color='black')
axb1 = axb.twinx()
axb1.set_ylabel('Distance (mm)', color='blue')
axb1.grid(False)
axb1.set_xlabel('time (s)', color='black')
axb1.tick_params(axis='y', color='blue', labelcolor= 'blue')
axb1.spines.left.set_position(("axes", 1.08))

line2, = axb.plot(t, Favg, 'k-')
line2b, = axb1.plot(t, Davg, 'b-')

plt.show()






diff_D = abs(np.diff(Davg, prepend=Davg[0]))

diff_t = np.diff(tavg, prepend=tavg[0])


Favg=np.array(Favg)
tavg=np.array(tavg)
mu = diff_D/diff_t
idx = mu >= 1e-7
mu = mu[idx]
favg = Favg[idx]
tavg = tavg[idx]

muavg=np.nanmean(mu)
print(muavg)



####this section uses stokes law to calclulate viscosity######
# Vraw=Favg/((pi_6)*(mu)*(Reff))

# Vavg = Vraw.mean()
# print(Vavg)
# stdV=np.std(Vraw)
# print(stdV)


# i = len(Vraw)
# lent=len(tavg)
# Diff=lent-i
# tavg=tavg[Diff:]

# fig= plt.figure(figsize=(10,10))
# ax1 = fig.add_subplot()
# ax1.plot(tavg, Vraw, '--', color ='black', markerfacecolor = 'none', markeredgecolor = 'k' , markersize = 15)
# plt.show()




# fig= plt.figure(figsize=(10,10))
# ax1 = fig.add_subplot()
# ax1.plot(tavg, Vmavg, '--', color ='black', markerfacecolor = 'none', markeredgecolor = 'k' , markersize = 15)
# ax2 = ax1.twinx()
# ax2.plot(tavg, Favg)
# plt.show()



# mean = np.mean(Vraw, axis=0)
# sd = np.std(Vraw, axis=0)

# # final_list = [x for x in Vraw if (x > mean - 2 * sd)]
# # final_list = [x for x in final_list if (x < mean + 2 * sd)]

# Vconf = [x for x in Vraw if (x > mean - sd)]
# Vconf = [x for x in Vconf if (x < mean + sd)]
# print(Vconf)

# Length = len(Vconf)
###################################################################
#######this section uses calibration procedure to calculate viscosity#################
F_RPen = favg/mu
print(F_RPen)


lowf =[]
medf =[]
highf =[] 

for val in F_RPen:
    if val <= 2000:
        lowf.append(float(val))
        pd.DataFrame(lowf)
    if val >= 2001 and val <=15000:
        medf.append(float(val))
        pd.DataFrame(medf)
        #print(medf)  
    if val >= 15001:
        highf.append(float(val))
        pd.DataFrame(highf)
        #print(highf) 
        
        
        #print("true") 
lowf = pd.Series(lowf)
#lowf = lowf
low_VCPen= ((lowf*1.736)-432.49)
#low_VCN19 =pd.DataFrame(low_VCN19)
medf = pd.Series(medf)
#medf = medf

med_VCPen= ((medf*2.7504)-223.8)
#med_VCN19 =pd.DataFrame(med_VCN19)
highf = pd.Series(highf)
#highf = highf
high_VCPen= ((highf*1.8734)+33905)

#VCPen = ([high_VCPen + low_VCPen + med_VCPen])
VCPen = pd.concat([high_VCPen, low_VCPen, med_VCPen])
#VCPen= (VCPen[0])
print(VCPen)


meancal = np.mean(VCPen, axis=0)
sdcal = np.std(VCPen, axis=0)

Vconfcal = [x for x in VCPen if (x > meancal - sdcal)]
Vconfcal = [x for x in VCPen if (x < meancal + sdcal)]
print(Vconfcal)

Lengthcal = len(Vconfcal)

Vmavgcal =moving_average(Vconfcal, window_size)

Length_2cal = len(Vmavgcal)




x2cal= list(range(0,Length_2cal))
Dstart=D[0]
Dend=D.iloc[-1]
dis_tot = (Dstart-Dend)#/1000
z= len(x2cal)
zz= dis_tot/z


    
xz= np.linspace(0,dis_tot,z)




plt.plot(x2cal, Vmavgcal, 'o-', color ='black', markerfacecolor = 'none', markeredgecolor = 'k' , label= 'vcal_smooth')
#plt.plot(xcal, Vconfcal, 'o-', color ='red', markerfacecolor = 'none', markeredgecolor = 'r' , label= 'vcal_raw')
#plt.plot(x2, Vmavg, 'o-', color ='green', markerfacecolor = 'none', markeredgecolor = 'g' , label= 'Viscosity_smooth')
#plt.plot(x, Vconf, 'o-', color ='blue', markerfacecolor = 'none', markeredgecolor = 'b' , label= 'Viscosity_raw')
plt.legend(loc="upper left")
plt.ylabel('Viscosity Pas')
plt.xlabel('data (n)')
  #label="Viscosity vs time ")
plt.show()


#plt.plot(x2cal, Vmavgcal, 'o-', color ='black', markerfacecolor = 'none', markeredgecolor = 'k' , label= 'vcal_smooth')
plt.plot(x2cal, Vconfcal, 'o-', color ='red', markerfacecolor = 'none', markeredgecolor = 'r' , label= 'vcal_raw')
#plt.plot(x2, Vmavg, 'o-', color ='green', markerfacecolor = 'none', markeredgecolor = 'g' , label= 'Viscosity_smooth')
#plt.plot(x, Vconf, 'o-', color ='blue', markerfacecolor = 'none', markeredgecolor = 'b' , label= 'Viscosity_raw')
plt.legend(loc="upper left")
plt.ylabel('Viscosity Pas')
plt.xlabel('data (n)')



plt.show()



###export data into .txt files 
np.savetxt("exported_cal_dat.txt", np.c_[x2cal, Vmavgcal, xz]), #thisT])
np.savetxt("exporteds_stat_cal_dat.txt", np.c_[meancal, sdcal]), #thisT])


plt.plot(xz, Vmavgcal, 'o-', color ='black', markerfacecolor = 'none', markeredgecolor = 'k' , label= 'vcal_to_distance')
plt.legend(loc="upper left")
plt.ylabel('Viscosity Pas')
plt.xlabel('lenght (m)')
plt.show()

