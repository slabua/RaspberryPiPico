# -*- coding: utf-8 -*-
"""BH1750FVI Ambient Light I2C Sensor
   Micropython Driver for the Raspberry Pi Pico.
"""

__author__ = "Salvatore La Bua"
__copyright__ = "Copyright 2025, Salvatore La Bua"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Salvatore La Bua"
__email__ = "slabua@gmail.com"
__status__ = "Development"

from machine import I2C, Pin
from utime import sleep, sleep_ms

I2C_ADDRESS = 0x23
CMD_CONT_HIGH_RES_MODE = 0x10  # Continuous high resolution mode

# Initialize I2C (I2C0 on GPIO 0 = SDA, GPIO 1 = SCL)
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)


def read_lux():
    # Send measurement command
    i2c.writeto(I2C_ADDRESS, bytes([CMD_CONT_HIGH_RES_MODE]))
    sleep_ms(20)  # Wait for measurement

    # Read 2 bytes of data
    data = i2c.readfrom(I2C_ADDRESS, 2)
    raw = (data[0] << 8) | data[1]
    lux = raw / 1.2
    return lux


while True:
    lux = read_lux()
    print("LUX: {:.2f} lx".format(lux))
    sleep(0.5)
