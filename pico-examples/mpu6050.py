from imu import MPU6050
from machine import Pin, I2C
from time import sleep

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

print(i2c.scan())
imu = MPU6050(i2c)
imu.accel_range = 0
imu.gyro_range = 0
# imu.filter_range = 0

period = 0.01

print(imu.accel_range, imu.gyro_range)

while True:
    # print(imu.accel.xyz,imu.gyro.xyz,imu.temperature,end='\r')

    # Read sensor data
    aX = imu.accel.x
    aY = imu.accel.y
    aZ = imu.accel.z
    gX = imu.gyro.x
    gY = imu.gyro.y
    gZ = imu.gyro.z
    tem = imu.temperature
    print(aX, "\t", aY, "\t", aZ, "\t", gX, "\t", gY,
          "\t", gZ, "\t", tem, "        ", end="\r")

    sleep(period)
