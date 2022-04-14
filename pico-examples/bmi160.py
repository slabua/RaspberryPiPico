from machine import Pin, I2C
from BMI160 import BMI160_I2C
from time import sleep_ms

# i2c = I2C(sda=Pin(32), scl=Pin(33))
i2c = I2C(0, sda=Pin(0), scl=Pin(1))
bmi160 = BMI160_I2C(i2c)

while True:
    print("{0:>8}{1:>8}{2:>8}{3:>8}{4:>8}{5:>8}".format(*bmi160.getMotion6()), end='\r')
    sleep_ms(1000//25)
