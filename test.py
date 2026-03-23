from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)

kit.servo[0].set_pulse_width_range(570,2390)
try:
    while True:
        angle = int(input("Input an angle between 0 and 180: "))
        kit.servo[0].angle = angle

except KeyboardInterrupt:
    print("Program terminated!")
