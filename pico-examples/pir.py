from machine import Pin
import time

led = Pin(25, Pin.OUT)
pir = Pin(22, Pin.IN, Pin.PULL_UP)

while True:
    print(pir.value())
    if pir.value():
        led.toggle()
    time.sleep(0.15)
