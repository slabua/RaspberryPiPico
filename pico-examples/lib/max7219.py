"""
MicroPython max7219 cascadable 8x8 LED matrix driver

Licensed under MIT, found in LICENSE.txt
    Copyright (c) 2017 Mike Causer
    Copyright (c) 2022 Leo Spratt

    Added 7 segments class from https://github.com/JennaSys/micropython-max7219
"""
from framebuf import FrameBuffer, MONO_HLSB
from machine import Pin, SPI
from micropython import const
from max7219.seven_segment_ascii import get_char2
import utime


_NOOP = const(0)
_DIGIT0 = const(1)
_DECODEMODE = const(9)
_INTENSITY = const(10)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)


MAX7219_DIGITS = 8

MAX7219_REG_NOOP = 0x0
MAX7219_REG_DIGIT0 = 0x1
MAX7219_REG_DIGIT1 = 0x2
MAX7219_REG_DIGIT2 = 0x3
MAX7219_REG_DIGIT3 = 0x4
MAX7219_REG_DIGIT4 = 0x5
MAX7219_REG_DIGIT5 = 0x6
MAX7219_REG_DIGIT6 = 0x7
MAX7219_REG_DIGIT7 = 0x8
MAX7219_REG_DECODEMODE = 0x9
MAX7219_REG_INTENSITY = 0xA
MAX7219_REG_SCANLIMIT = 0xB
MAX7219_REG_SHUTDOWN = 0xC
MAX7219_REG_DISPLAYTEST = 0xF

SPI_BUS = 1  # hardware SPI
SPI_BAUDRATE = 100000
SPI_CS = 0  # D3


class Matrix8x8(FrameBuffer):
    def __init__(self, spi, cs, num, format=MONO_HLSB):
        """
        Driver for cascading MAX7219 8x8 LED matrices.

        >>> from machine import Pin, SPI
        >>> from max7219 import Matrix8x8
        >>> spi = SPI(1)
        >>> display = Matrix8x8(spi, Pin('X5'), 4)
        >>> display.text('1234')
        >>> display.show()

        """
        self._spi = spi
        self._cs = cs
        self._cs.init(self._cs.OUT, True)
        self._num = num
        self._buffer = bytearray(8 * self._num)

        super().__init__(self._buffer, 8 * self._num, 8, format)

        self._write_init()

    def _write(self, command, data):
        self._cs(0)
        for _ in range(self._num):
            self._spi.write(bytearray([command, data]))
        self._cs(1)

    def _write_init(self):
        for command, data in (
            (_SHUTDOWN, 0),
            (_DISPLAYTEST, 0),
            (_SCANLIMIT, 7),
            (_DECODEMODE, 0),
            (_SHUTDOWN, 1),
        ):
            self._write(command, data)

    def brightness(self, value):
        if not 0 <= value <= 15:
            raise ValueError("Brightness out of range")
        self._write(_INTENSITY, value)

    def text(self, s, x=0, y=0, c=1):
        super().text(s, x, y, c)

    def text_from_glyph(self, s, glyphs, x_offset=0, y_offset=0):
        col = 0
        for char in s:
            glyph = glyphs.get(char)

            if glyph:
                for y in range(8):
                    for x in range(8):
                        self.pixel(x+col+x_offset, y+y_offset, glyph[y][x])
            else:
                self.text(char, col+x_offset, y_offset)

            col += 8

    def show(self):
        for y in range(8):
            self._cs(0)
            for m in range(self._num):
                self._spi.write(bytearray([_DIGIT0 + y, self._buffer[(y * self._num) + m]]))
            self._cs(1)

    def zero(self):
        self.fill(0)

    def shutdown(self):
        self._write(_SHUTDOWN, 0)

    def wake(self):
        self._write(_SHUTDOWN, 1)

    def test(self, enable=True):
        self._write(_DISPLAYTEST, int(enable))


class SevenSegment:
    def __init__(self, digits=8, scan_digits=MAX7219_DIGITS, baudrate=SPI_BAUDRATE, cs=SPI_CS, spi_bus=SPI_BUS, reverse=False):
        """
        Constructor:
        `digits` should be the total number of individual digits being displayed
        `scan_digits` is the number of digits each individual max7219 displays
        `baudrate` defaults to 100KHz, note that excessive rates may result in instability (and is probably unnecessary)
        `cs` is the GPIO port to use for the chip select line of the SPI bus - defaults to GPIO 0 / D3
        `spi_bus` is the SPI bus on the controller to utilize - defaults to SPI bus 1
        `reverse` changes the write-order of characters for displays where digits are wired R-to-L instead of L-to-R
        """

        self.digits = digits
        self.devices = -(-digits // scan_digits)  # ceiling integer division
        self.scan_digits = scan_digits
        self.reverse = reverse
        self._buffer = [0] * digits
        self._spi = SPI(spi_bus, baudrate=baudrate, polarity=0, phase=0)
        self._cs = Pin(cs, Pin.OUT, value=1)

        self.command(MAX7219_REG_SCANLIMIT, scan_digits - 1)  # digits to display on each device  0-7
        self.command(MAX7219_REG_DECODEMODE, 0)   # use segments (not digits)
        self.command(MAX7219_REG_DISPLAYTEST, 0)  # no display test
        self.command(MAX7219_REG_SHUTDOWN, 1)     # not blanking mode
        self.brightness(7)                        # intensity: range: 0..15
        self.clear()

    def command(self, register, data):
        """Sets a specific register some data, replicated for all cascaded devices."""
        self._write([register, data] * self.devices)

    def _write(self, data):
        """Send the bytes (which should be comprised of alternating command, data values) over the SPI device."""
        self._cs.off()
        self._spi.write(bytes(data))
        self._cs.on()

    def clear(self, flush=True):
        """Clears the buffer and if specified, flushes the display."""
        self._buffer = [0] * self.digits
        if flush:
            self.flush()

    def flush(self):
        """For each digit, cascade out the contents of the buffer cells to the SPI device."""
        buffer = self._buffer.copy()
        if self.reverse:
            buffer.reverse()

        for dev in range(self.devices):
            if self.reverse:
                current_dev = self.devices - dev - 1
            else:
                current_dev = dev

            for pos in range(self.scan_digits):
                self._write([pos + MAX7219_REG_DIGIT0, buffer[pos + (current_dev * self.scan_digits)]] + ([MAX7219_REG_NOOP, 0] * dev))

    def brightness(self, intensity):
        """Sets the brightness level of all cascaded devices to the same intensity level, ranging from 0..15."""
        self.command(MAX7219_REG_INTENSITY, intensity)

    def letter(self, position, char, dot=False, flush=True):
        """Looks up the appropriate character representation for char and updates the buffer, flushes by default."""
        value = get_char2(char) | (dot << 7)
        self._buffer[position] = value

        if flush:
            self.flush()

    def text(self, text):
        """Outputs the text (as near as possible) on the specific device."""
        self.clear(False)
        text = text[:self.digits]  # make sure we don't overrun the buffer
        for pos, char in enumerate(text):
            self.letter(pos, char, flush=False)

        self.flush()

    def number(self, val):
        """Formats the value according to the parameters supplied, and displays it."""
        self.clear(False)
        strval = ''
        if isinstance(val, (int, float)):
            strval = str(val)
        elif isinstance(val, str):
            if val.replace('.', '', 1).strip().isdigit():
                strval = val

        if '.' in strval:
            strval = strval[:self.digits + 1]
        else:
            strval = strval[:self.digits]

        pos = 0
        for char in strval:
            dot = False
            if char == '.':
                continue
            else:
                if pos < len(strval) - 1:
                    if strval[pos + 1] == '.':
                        dot = True
                self.letter(pos, char, dot, False)
                pos += 1

        self.flush()

    def scroll(self, rotate=True, reverse=False, flush=True):
        """Shifts buffer contents left or right (reverse), with option to wrap around (rotate)."""
        if reverse:
            tmp = self._buffer.pop()
            if rotate:
                self._buffer.insert(0, tmp)
            else:
                self._buffer.insert(0, 0x00)
        else:
            tmp = self._buffer.pop(0)
            if rotate:
                self._buffer.append(tmp)
            else:
                self._buffer.append(0x00)

        if flush:
            self.flush()

    def message(self, text, delay=0.4):
        """Transitions the text message across the devices from left-to-right."""
        self.clear(False)
        for char in text:
            utime.sleep(delay)
            self.scroll(rotate=False, flush=False)
            self.letter(self.digits - 1, char)