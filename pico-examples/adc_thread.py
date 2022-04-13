import _thread
from machine import ADC, Pin, PWM
from time import sleep

adc = ADC(Pin(26))
pwm = PWM(Pin(25))
pwm.freq(1000)
#led = Pin(25, Pin.OUT)

steps_slow = 128
steps_fast = 1024

brightness_low = 1024
brightness_high = 65025

reading = 0
n_steps = 0

flag = False


def steps(value):
    n_steps = int(value / 65535 * steps_fast)
    if n_steps < steps_slow:
        n_steps = steps_slow
    return n_steps


def pulse(n_steps, br_high, br_low):
    for duty in range(br_low, br_high, int(n_steps**2)):
        pwm.duty_u16(duty)
        sleep(0.0002)
    for duty in range(br_high, br_low, -int(n_steps**1)):
        pwm.duty_u16(duty)
        sleep(0.0025)
    #flag = True


def toggle(freq):
    led.toggle()
    sleep(freq/100000)
    led.toggle()


def toggle_thread(freq):
    led.toggle()
    sleep(freq/100000)
    #led.toggle()
    flag = True


def reading_thread():
    global reading
    while True:
        reading = adc.read_u16()
        #print("1thread:" + str(reading))
        #print(" -ack")
        sleep(1.0)
    flag = True


_thread.start_new_thread(reading_thread, ())


while not flag:
    
    n_steps = steps(reading)
    pulse(n_steps, brightness_high, brightness_low)
    
    #print("0thread:" + str(n_steps))
    sleep(0.05)
    
    print(reading, n_steps)
    
print("Flag is True")
