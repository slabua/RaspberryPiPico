from machine import Pin, SPI
import os
import sdcard
import time

cs_pin = Pin(28, Pin.OUT)

spi = SPI(
    id=1,
    sck=Pin(10, Pin.OUT),
    mosi=Pin(11, Pin.OUT),
    miso=Pin(8, Pin.OUT),
)

sd = sdcard.SDCard(spi, cs_pin)
os.mount(sd, "/sd")
os.chdir("sd")
os.listdir()

file = open("/sd/test.txt", "w")
file.write(str(time.localtime()))
file.close()

print(open("test.txt").read())
