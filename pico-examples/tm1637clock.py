from machine import Pin
import tm1637
import utime


tm = tm1637.TM1637Decimal(clk=Pin(5), dio=Pin(3))
tm.brightness(7)

segs = [64, 2, 4, 8, 16, 32, 1]
dots = False

now = utime.localtime()
m0 = now[4]
s0 = now[5]

while True:
    now = utime.localtime()
    h = now[3]
    m = now[4]
    s = now[5]

    # if m != m0:
    if s % 30 == 0:
        for seg in segs:
            tm.write([seg, seg, seg, seg])
            utime.sleep(0.05)

    dots = not dots

    m0 = m
    s0 = s

    tm.numbers(h, m, dots)
    utime.sleep(0.5)
