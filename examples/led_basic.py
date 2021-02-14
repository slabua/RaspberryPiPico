from machine import Pin
from time import sleep

led = Pin(25, Pin.OUT)

led.value(1)
sleep(2)
led.value(0)
