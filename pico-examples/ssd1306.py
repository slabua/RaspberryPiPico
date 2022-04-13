from machine import Pin, I2C
from lib.ssd1306 import SSD1306_I2C

import machine
from time import sleep

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

w = 128
h = 32

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
print(i2c.scan())
addr = i2c.scan()[0]
oled = SSD1306_I2C(w, h, i2c, addr)

# oled.contrast(255) 
# oled.fill(1)
# oled.text(str(addr), 0, 0, 1)
# oled.show()

# oled.invert(1)
oled.fill(0)
oled.fill_rect(0, 0, 32, 32, 1)
oled.fill_rect(2, 2, 28, 28, 0)
oled.vline(9, 8, 22, 1)
oled.vline(16, 2, 22, 1)
oled.vline(23, 8, 22, 1)
oled.fill_rect(26, 24, 2, 4, 1)
oled.text('MicroPython', 40, 0, 1)
oled.text('SSD1306', 40, 12, 1)
oled.text('OLED 128x32', 40, 24, 1)

oled.scroll(-1, 0)
oled.show()

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    # print(temperature)
    oled.vline(127, 0, 64, 0)
    h = 31 - round(temperature)*4 + 96
    print(h)
    oled.pixel(127, h, 1)
    oled.show()
    sleep(0.01)
    oled.scroll(-1, 0)
    oled.show()
