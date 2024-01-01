from lcd_i2c import LCD
from machine import I2C, Pin, ADC
from utime import sleep

# PCF8574 on 0x50
I2C_ADDR = 0x27     # DEC 39, HEX 0x27
NUM_ROWS = 4
NUM_COLS = 20

# define custom I2C interface, default is 'I2C(0)'
# check the docs of your device for further details and pin infos
i2c = I2C(0, scl=Pin(13), sda=Pin(12), freq=8000)  # 800000
lcd = LCD(addr=I2C_ADDR, cols=NUM_COLS, rows=NUM_ROWS, i2c=i2c)

lcd.begin()


lcd.set_cursor(0, 0)
for i in range(176, 176 + 20):
    lcd.print(chr(i))
lcd.set_cursor(0, 1)
for i in range(176 + 20, 176 + 40):
    lcd.print(chr(i))
lcd.set_cursor(0, 2)
for i in range(176 + 40, 176 + 60):
    lcd.print(chr(i))
lcd.set_cursor(0, 3)
for i in range(176 + 60, 176 + 80):
    lcd.print(chr(i))

lcd.clear()

lcd.set_cursor(0, 0)
lcd.print("Hello World 0")
lcd.set_cursor(0, 1)
lcd.print("Hello World 1")
lcd.set_cursor(0, 2)
lcd.print("Hello World 2")
lcd.set_cursor(0, 3)
lcd.print("Hello World 3")


sensor_temp = ADC(4)
conversion_factor = 3.3 / (65535)

r = 0
while True:
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = round(27 - (reading - 0.706) / 0.001721, 3)
    print(temperature)
    lcd.set_cursor(0, r)
    lcd.print("                    ")
    lcd.set_cursor(0, r)
    # lcd.print("C " + str(temperature))
    lcd.print(f"{str(temperature) + " C":<18}")
    sleep(1)
    # lcd.clear()
    r = (r + 1) % 4
