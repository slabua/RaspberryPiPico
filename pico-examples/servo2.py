from machine import Pin, PWM
import utime

servo = PWM(Pin(2))

servo.freq(50)

# .duty_16(#) takes values of 0 to 65535 for duty cycle of 0 to 100
# SG90 has 2 per cent duty cycle for 0 degrees, 12 per cent for 180.
# So a .duty_u16 value of c.1350 is zero degrees; 8200 is 180 degrees.

while True:
    for i in range((8400-1600)/20):
        servo.duty_u16(int(1600+i*20))
        utime.sleep(0.001)
    for i in range((8400-1600)/20):
        servo.duty_u16(int(8400-i*20))
        utime.sleep(0.005)
