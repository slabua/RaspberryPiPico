from machine import Pin, PWM
from time import sleep


sensor_temp = machine.ADC(4)

pwm = machine.PWM(machine.Pin(25))
pwm.freq(1000)

conversion_factor = 3.3 / (65535)

threshold_min = 19
threshold_max = 23

steps_slow = 16
steps_fast = 1024

brightness_low = 0
brightness_high = 65025


def temperature(reading):
    return 27 - (reading - 0.706)/0.001721


def steps(temp, th_min, th_max, steps_slow, steps_fast):
    if temp < th_min:
        n_steps = steps_slow
    elif temp > th_max:
        n_steps = steps_fast
    else:
        n_steps = temp
    
    return n_steps


def pulse(n_steps, br_high, br_low):
    for duty in range(br_low, br_high, int(n_steps**2)):
        pwm.duty_u16(duty)
        sleep(0.001)
    for duty in range(br_high, br_low, -int(n_steps**3)):
        pwm.duty_u16(duty)
        sleep(0.05)


while True:
    reading = sensor_temp.read_u16() * conversion_factor

    temp = temperature(reading)
    print(temp)
    
    n_steps = steps(temp, threshold_min, threshold_max, steps_slow, steps_fast)
    
    pulse(n_steps, brightness_high, brightness_low)

