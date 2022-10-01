from machine import Pin, PWM
from servo import Servo
import utime


servo = Servo(2)

while True:
    for angle in range(180):
        servo.value(angle - 90)
        utime.sleep(0.005)
    for angle in range(180):
        servo.value(90 - angle)
        utime.sleep(0.005)
