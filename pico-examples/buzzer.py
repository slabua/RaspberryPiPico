from machine import Pin, PWM
from utime import sleep
import urandom


BUZZER_PIN = 0
buzzer = PWM(Pin(BUZZER_PIN, Pin.OUT))


def play_tone(frequency, volume, duration):
    buzzer.duty_u16(volume)
    buzzer.freq(frequency)
    sleep(duration)


def mute(pause):
    buzzer.duty_u16(0)
    sleep(pause)


while True:
    tone = urandom.randrange(500, 5000)
    play_tone(tone, 5000, 0.01)
    mute(0.08)
