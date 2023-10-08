from machine import Pin, SPI
# import math
import max7219
from time import sleep

spi = SPI(0, baudrate=8000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
cs = Pin(5, Pin.OUT)

n = 8
display = max7219.Matrix8x8(spi, cs, n)
display.brightness(1)

text1 = "Hello"
text2 = "World"

GLYPHS = {
    "H": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
    ],
}

length = len(text1) + 1 + len(text2)
# repeat = math.ceil(n / length)

display.fill(0)
display.show()

while True:
    # for x in range(n * 8, -(length * 8) - (n * 8), -1):
    for x in range(n * 8, -(length * 8), -1):
        display.fill(0)

        display.text(text1, x, 1, 1)
        display.text_from_glyph("H", GLYPHS, x + (len(text1) * 8), 0)
        display.text(text2, x + 9 + (len(text1) * 8), 1, 1)
        display.show()

        sleep(0.025)
