import machine
import neopixel
import time


PIN_NUM = 2
NUM_LEDS = 144
RGBW = False

np = neopixel.NeoPixel(machine.Pin(PIN_NUM), NUM_LEDS, bpp=4 if RGBW else 3, timing=1)


def demo(np):
    n = np.n

    # cycle
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (255, 255, 255)
        np.write()
        time.sleep_ms(25)

    # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

    # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
        np.write()
        time.sleep_ms(60)

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()


demo(np)
