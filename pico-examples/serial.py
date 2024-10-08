from machine import Pin, UART
import random
import sys
from utime import sleep

# Initialize UART0 with a baud rate of 9600
uart = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))
uart.init(bits=8, parity=None, stop=1)


def generate_random_number():
    return random.randint(0, 9)


while True:
    random_number = generate_random_number()
    sys.stdout.write(f"{random_number}\n")
    # uart.write(str(random.randint(0, 9)))
    # uart.write(str(utime.localtime()) + "\n")
    # uart.write(f'{random_number}\n')
    # sys.stdout.flush()  # Ensure the output is written immediately
    sleep(1)

"""
while True:
    print(uart.read(1))
"""
