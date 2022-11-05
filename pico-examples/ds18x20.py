import machine
import onewire
import ds18x20
import time

ds_pin = machine.Pin(11)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()
print('Found a ds18x20 device')
print(roms)

time.sleep_ms(750)

while True:
    ds_sensor.convert_temp()
    time.sleep_ms(750)
    for i in range(len(roms)):
        print("T" + str(i) + ": " + str(ds_sensor.read_temp(roms[i])))
    # time.sleep(0.15)
