from machine import Pin, PWM
from time import sleep

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

pwm = machine.PWM(machine.Pin(25))
pwm.freq(1000)

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    
    temperature = 27 - (reading - 0.706)/0.001721
    print(temperature)
    
    if temperature < 19:
        steps = 16
    elif temperature > 23:
        steps = 1024
    else:
        steps = temperature
    
    for duty in range(0, 65025, int(steps**2)):
        pwm.duty_u16(duty)
        sleep(0.001)
    for duty in range(65025, 0, -int(steps**3)):
        pwm.duty_u16(duty)
        sleep(0.05)

        