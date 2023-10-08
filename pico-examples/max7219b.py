from machine import Pin, SPI
import max7219
import time

spi = SPI(0, baudrate=8000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
cs = Pin(5, Pin.OUT)

n = 4
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

display.fill(0)
display.show()

while True:
    for x in range(n * 8, -(len(text1) + 1 + len(text2)) * 8, -1):
        display.fill(0)

        display.text(text1, x, 1, 1)
        display.text_from_glyph("H", GLYPHS, x + (len(text1) * 8), 0)
        display.text(text2, x + 9 + (len(text1) * 8), 1, 1)
        display.show()

        time.sleep(0.025)
