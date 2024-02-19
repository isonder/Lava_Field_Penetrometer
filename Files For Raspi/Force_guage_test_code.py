
import serial
import keyboard
import time
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=38400, bytesize=8, timeout =2, stopbits= serial.STOPBITS_ONE)

fd = open('force_dump.txt', mode='w')
fd.write('Time, Force\n')
t0 = time.time()
while True:
    t = time.time() - t0
    ser.write("x".encode('Ascii'))
    receive = ser.readline().decode('Ascii')
    print(receive)
    fd.write(f"{t:.4f} {receive[1:]}\n")# write file includes multiples variables, t is time as float soecified to 4 decimals
    time.sleep(0.1)

    if keyboard.is_pressed('q'):
         print("User need to Quit the application")
         fd.close()
         break
ser.close

