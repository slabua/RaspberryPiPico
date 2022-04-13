from machine import Pin, PWM
from time import sleep

pwm = PWM(Pin(25))
pwm.freq(1000)

while True:
    for duty in range(1024, 65025, 2):
        pwm.duty_u16(duty)
        sleep(0.0001)
    for duty in range(65025, 1024, -4):
        pwm.duty_u16(duty)
        sleep(0.0005)
