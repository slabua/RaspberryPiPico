import copy
from machine import Pin, SPI
from max7219 import Matrix8x8
import random
import utime

spi = SPI(0, baudrate=8000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
cs = Pin(5, Pin.OUT)
n = 8

brightness_default = 0
brightness_glitch = 1

display = Matrix8x8(spi=spi, cs=cs, num=n)

# change brightness 1-15
display.brightness(brightness_default)

# clear display
display.zero()
display.show()
# show text using FrameBuffer's font
# display.text("TEST")
# display.show()

GLYPHS = {
    "X": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    "O": [
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 1, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 1, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
    ],
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
    "I": [
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
    ],
}


def glitch(glyph, glitch_array=[]):
    # Adapted from
    # https://twitter.com/aaa_tu/status/1596386555706298368
    # https://twitter.com/aaa_tu/status/1596550426073391105
    _has_glitched = False
    if glitch_array:
        _glitch_array = glitch_array
    else:
        _glitch_array = []
    for i, r in enumerate(glyph):
        if glitch_array:
            n = glitch_array[i]
        else:
            n = random.choice([0, 0, 0, 0, 0, 0, 0, 0, 1, -2, 3])
            # n = random.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            #                   0, 0, 0, 0, 0, 0, 1, 2, -1, -2])
            # n = random.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            #                   0, 0, 0, 0, 0, 1, 2, 3, -1, -2, -3])
            _glitch_array.append(n)
        if n != 0:
            _has_glitched = True

        glyph[i] = r[n:] + r[:n]

    return glyph, _has_glitched, _glitch_array


def glitch_all_glyphs(glyphs):
    is_first_item = True
    for gk in glyphs.keys():
        if is_first_item:
            is_first_item = False
            glyphs[gk], _has_glitched, _glitch_array = glitch(glyphs[gk])
        else:
            glyphs[gk] = glitch(glyphs[gk], _glitch_array)[0]

    return _has_glitched

def copydict(dict1, dict2):
    for k in dict1.keys():
        dict2[k] = copy.deepcopy(dict1[k])

TEXT = "HAHIOHBH"

count = 0
while count < 5:
    GLYPHS2 = copy.deepcopy(GLYPHS)

    display.brightness(brightness_default)

    display.text_from_glyph(TEXT, GLYPHS2)
    display.show()
    utime.sleep(random.uniform(1, 3))

    has_glitched = glitch_all_glyphs(GLYPHS2)

    if has_glitched:
        display.brightness(brightness_glitch)

    display.text_from_glyph(TEXT, GLYPHS2)
    display.show()
    utime.sleep(0.05)
    count += 1


count = 0
length = 8
GLYPHS2 = {}
while count < 2:
    GLYPHS2 = copy.deepcopy(GLYPHS)
    # copydict(GLYPHS, GLYPHS2)
    # GLYPHS2 = GLYPHS.copy()
    # for x in range(n * 8, -(length * 8) - (n * 8), -1):
    for x in range(n * 8, -(length * 8), -1):
        display.fill(0)
        has_glitched = glitch_all_glyphs(GLYPHS2)
        display.text_from_glyph("HHABIO", GLYPHS2, x, 0)
        display.show()
        GLYPHS2 = copy.deepcopy(GLYPHS)
        # copydict(GLYPHS, GLYPHS2)

        display.fill(0)
        display.text_from_glyph("HHABIO", GLYPHS2, x, 0)
        display.show()
        # utime.sleep(0.005)
    count += 1
