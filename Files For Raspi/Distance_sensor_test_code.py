
import keyboard
import board
import busio

import adafruit_vl53l0x

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)
#vl53 = adafruit_vl53l0x.VL53L0X(i2c,9x20)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

# Optionally adjust the measurement timing budget to change speed and accuracy.
# See the example here for more details:
#   https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
# For example a higher speed but less accurate timing budget of 20ms:
# vl53.measurement_timing_budget = 20000
# Or a slower but more accurate timing budget of 200ms:
# vl53.measurement_timing_budget = 200000
# The default timing budget is 33ms, a good compromise of speed and accuracy.

t0 = time.time()


# Main loop will read the range and print it every second.

while True:
    t = time.time() - t0
    d= ("Range: {0}mm".format(vl53.range))
    rd.write(f"{t:.4f} {d[1:]}\n")# write file includes multiples variables, t is time as float soecified to 4 decimals
    print(d)
    time.sleep(1.0)
    
    if keyboard.is_pressed('q'):
        print("User need to Quit the application")
        rd.close()
        break
d.closeq
qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq
