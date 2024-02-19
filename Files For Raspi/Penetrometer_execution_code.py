import RPi.GPIO as GPIO #GPIO pins used for switches
import time
import datetime #used to timestamp output files
from datetime import datetime
import board 
import busio
import serial
import os
import adafruit_vl53l0x # this is specific to the time of flight sensor used
import numpy as np
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askdirectory

Wd = "Set your working directory here!"
os.chdir(Wd)

from adafruit_ht16k33.segments import Seg7x4 #this is used for specific LED display

i2c = board.I2C() #LED board is connected to i2c pins
display = Seg7x4(i2c) #again using specific LED size for display

i2c = busio.I2C(board.SCL, board.SDA) #here we set up the time of flight distance sensor to also be connected with i2c pins 

vl53 = adafruit_vl53l0x.VL53L0X(i2c) # distance sensor i2c

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) #setup flip switch at GPIO pin 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) #setup flip switch at gpio pin 12
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=38400, bytesize=8, timeout =2, stopbits= serial.STOPBITS_ONE) #create a serial connection to the force guage via usb

while True: #starts the main loop
    switch1 = GPIO.input(12) #defines switch 1
    switch2 = GPIO.input(16) #defines switch 2
    
    if switch1 == True: #first condition iteration if switch 1 is flipped down then continue
        display.print("IDLE") #display this text on LED
        print('Waiting') #print this text on terminal 
        time.sleep(0.5)
    else: #if first condition is not met ie. switch 1 is flipped up, then proceed below
        
        if switch2 == True: #secondary condition if switch 2 is down
            D = datetime.now().strftime('%H:%M')#define datetime as hours and minutes for display LED
            #display.print("PUSH")#text to display on LED
            display.print(D) #display time as hour minutes on LED

            print('ready') #print text to terminal
            time.sleep(0.5)
        else: #if swtich 2 gets flipped up do the following
            switch1 = GPIO.input(12)#redefine switch1 so that loop can be exited if first swithc is flipped
            if switch1 == True:
                break
            filename = f"{time.strftime('%Y-%m-%d_%H-%M-%S')}_log.txt"# create file name with date time stamp
            folder1 = "insert your working directory here!" # stores files on sd
            
            filename1 = folder1 + filename
        
            dd1 = open(filename1, mode='w') #create file dd1
            dd1.write('Time(s) Force(N) Distance_mm\n') #add headers of data file
           
            print("created" + filename1)
            t0 = time.time() #creates a time starting point at 0
            i = 0
            while switch2 == False: #while the switch 2 is flipped up, do the following

                i += 1
            
                t = time.time() - t0 #create time variable starting at 0
                d= ("Range: {0}mm".format(vl53.range)) #create distance variab;e from distance sensor
                d=float(vl53.range) #convert distance data to float type
                ser.write("x".encode('Ascii')) #send ascii x to force guage needed to recieve live data
                receive = ser.readline().decode('Ascii') #reads the live data lines from the force guage
                x=receive.split('\t') #splits the lines from the force guage and creates a variable x

                f=float(x[0]) #creates variabe; f for force as float of first value from force guage lines
                if x[2]=='Live Tension': #create a small condition that if tension is detected from readlines, make force negative value
                    f=f*-1
                F =("0%.1f" % f)

                display.print(F)
                dd1.write(f"{t:.4f} {f:.4f} {d:.4f}\n")
               
                print(t)
                dd1.flush()
               
                time.sleep(0.033)
                switch1=GPIO.input(12)
                switch2=GPIO.input(16)
                if switch1 == True:
                    break
