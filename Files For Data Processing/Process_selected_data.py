
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

p= path[-16:]


df= pd.read_csv(p, delim_whitespace=True)

df.columns = ['Time(s)', 'Distance_mm','Force(N)']
filename= p[:18]


t = df['Time(s)'] 

F = df['Force(N)']
D = df['Distance_mm']
Dmet = D/1000

df_length = len(df)
w = int((df_length)*0.2)

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w
Davg =moving_average(Dmet, w)
tavg = moving_average(t, w)
Favg = moving_average(F, w)

diff_D = abs(np.diff(Davg))

diff_t = np.diff(tavg)


fig= plt.figure(figsize=(10,10))
ax1 = fig.add_subplot()
ax1.plot(t, D, '--', color ='black', markerfacecolor = 'none', markeredgecolor = 'k' , markersize = 15)
ax2 = ax1.twinx()
ax2.plot(t, F, '--', color ='red', markerfacecolor = 'none', markeredgecolor = 'k' , markersize = 15)
ax3 = ax1.twinx()
ax3.plot(tavg, Davg, '-', color ='black', markerfacecolor = 'none', markeredgecolor = 'k' , markersize = 15)
ax4 = ax1.twinx()
ax4.plot(tavg, Favg, '-', color ='red', markerfacecolor = 'none', markeredgecolor = 'k' , markersize = 15)

plt.show()




Reff = 0.03825
Reff = Reff/2
mu = diff_D/diff_t
mu=mu[mu != 0]
mu=mu[mu >= 1.00e-07]
i = len(mu)
lenF=len(Favg)
Diff=lenF-i

muavg=np.nanmean(mu)
print(muavg)


Favg=Favg[Diff:]

Vraw=Favg/((pi_6)*(mu)*(Reff))

Vavg = Vraw.mean()
print(Vavg)
stdV=np.std(Vraw)
print(stdV)


i = len(Vraw)
lent=len(tavg)
Diff=lent-i
tavg=tavg[Diff:]







def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w
Vmavg =moving_average(Vraw, 30)
tavg = moving_average(tavg, 30)




mean = np.mean(Vraw, axis=0)
sd = np.std(Vraw, axis=0)



Vconf = [x for x in Vraw if (x > mean - sd)]
Vconf = [x for x in Vconf if (x < mean + sd)]
print(Vconf)

Length = len(Vconf)



x = list(range(0,Length))
print (x)




Vconf_length = len(Vconf)

w2 = int((Vconf_length)*0.2)
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


Vmavg =moving_average(Vconf, w2)

Length_2 = len(Vmavg)




x2= list(range(0,Length_2))


###implement the calibration procedure


F_RPen = Favg/mu
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

# final_list = [x for x in Vraw if (x > mean - 2 * sd)]
# final_list = [x for x in final_list if (x < mean + 2 * sd)]

Vconfcal = [x for x in VCPen if (x > mean - sd)]
Vconfcal = [x for x in VCPen if (x < mean + sd)]
print(Vconfcal)

Lengthcal = len(Vconfcal)



xcal = list(range(0,Lengthcal))
print (xcal)

# fig= plt.figure(figsize=(10,10))
# ax1 = fig.add_subplot()
# ax1.plot(xcal, Vconfcal, '--', color ='black', markerfacecolor = 'none', markeredgecolor = 'k' , markersize = 15)
# plt.show()


Vconfcal_length = len(Vconfcal)

w3 = int((Vconfcal_length)*0.2)
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


Vmavgcal =moving_average(Vconfcal, w3)

Length_2cal = len(Vmavgcal)




x2cal= list(range(0,Length_2cal))
Dstart=D[0]
Dend=D.iloc[-1]
dis_tot = (Dstart-Dend)/1000
z= len(x2cal)
zz= dis_tot/z


    
xz= np.linspace(0,dis_tot,z)

# ax1 = fig.add_subplot()

# axa1.set_xlabel('data (n)', color='black')
# axa1.set_ylabel('Viscosity_cal Pas', color='black')

# ax1.plot(x2cal, Vmavgcal, '--', color ='black', markerfacecolor = 'none', markeredgecolor = 'k' , markersize = 15)
# axa1.tick_params(axis='y', color='black', labelcolor= 'black')
# ax2 = ax1.twinx()
# ax2.set_ylabel('Viscosity_cal_smooth Pas', color='red')
# ax2.plot(xcal, Vconfcal, '--', color ='red', markerfacecolor = 'none', markeredgecolor = 'k' , markersize = 15)
# ax2.spines.left.set_position(("axes", 1.08))
# ax3 = ax1.twinx()
# ax3.set_ylabel('Viscosity_raw', color='green')
# ax3.plot(x2, Vmavg, '--', color ='green', markerfacecolor = 'none', markeredgecolor = 'k' , markersize = 15)
# ax2.spines.left.set_position(("axes", 2.08))
# plt.show()



plt.plot(x2cal, Vmavgcal, 'o-', color ='black', markerfacecolor = 'none', markeredgecolor = 'k' , label= 'vcal_smooth')
#plt.plot(xcal, Vconfcal, 'o-', color ='red', markerfacecolor = 'none', markeredgecolor = 'r' , label= 'vcal_raw')
plt.plot(x2, Vmavg, 'o-', color ='green', markerfacecolor = 'none', markeredgecolor = 'g' , label= 'Viscosity_smooth')
#plt.plot(x, Vconf, 'o-', color ='blue', markerfacecolor = 'none', markeredgecolor = 'b' , label= 'Viscosity_raw')
plt.legend(loc="upper left")
plt.ylabel('Viscosity Pas')
plt.xlabel('data (n)')
  #label="Viscosity vs time ")
plt.show()
#

#plt.plot(x2cal, Vmavgcal, 'o-', color ='black', markerfacecolor = 'none', markeredgecolor = 'k' , label= 'vcal_smooth')
plt.plot(xcal, Vconfcal, 'o-', color ='red', markerfacecolor = 'none', markeredgecolor = 'r' , label= 'vcal_raw')
#plt.plot(x2, Vmavg, 'o-', color ='green', markerfacecolor = 'none', markeredgecolor = 'g' , label= 'Viscosity_smooth')
plt.plot(x, Vconf, 'o-', color ='blue', markerfacecolor = 'none', markeredgecolor = 'b' , label= 'Viscosity_raw')
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
plt.xlabel('depth (m)')
plt.show()



















