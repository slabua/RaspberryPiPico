from imu import MPU6050
import time
from machine import Pin, I2C

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
print(i2c.scan())
imu = MPU6050(i2c)

while True:
    #print(imu.accel.xyz, imu.gyro.xyz, imu.temperature, end='\r')
    ax = round(imu.accel.x, 2)
    ay = round(imu.accel.y, 2)
    az = round(imu.accel.z, 2)
    gx = round(imu.gyro.x)
    gy = round(imu.gyro.y)
    gz = round(imu.gyro.z)
    temp = round(imu.temperature, 2)
    print(
        ax, "\t",
        ay, "\t",
        az, "\t",
        gx, "\t",
        gy, "\t",
        gz, "\t",
        temp, "        ",
        end="\r"
    )
