import network
import socket
from time import sleep

import machine
from picozero import pico_temp_sensor, pico_led

SSID = 'YOUR_SSID'
PASSWORD = 'YOUR_PASSWORD'

LAST_OCTET = 100


def connect():
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm=0xa11140)  # disable powersaving mode
    wlan.connect(SSID, PASSWORD)

    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)

    # Handle connection error
    # Error meanings
    # 0  Link Down
    # 1  Link Join
    # 2  Link NoIp
    # 3  Link Up
    # -1 Link Fail
    # -2 Link NoNet
    # -3 Link BadAuth
    # wlan_status = wlan.status()

    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')

    return wlan


def add_static_if(wlan, last_octet):
    ip, mask, gw, dns = wlan.ifconfig()
    ip = ip[:ip.rfind('.')+1] + str(last_octet)
    print(f'Static interface on {ip}')

    sta_if = network.WLAN(network.STA_IF)
    sta_if.ifconfig((ip, mask, gw, dns))

    return ip


def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(address)
    connection.listen(1)

    return connection


def webpage(temperature, state):
    # Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./1">
            <input type="submit" value="1" />
            </form>
            <form action="./0">
            <input type="submit" value="0" />
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temperature}</p>
            </body>
            </html>
            """

    return str(html)


def serve(connection):
    # Start a web server
    state = 'OFF'
    pico_led.off()
    temperature = 0

    while True:
        client, address = connection.accept()
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if '1' in request:
            pico_led.on()
            state = 'ON'
        elif '0' in request:
            pico_led.off()
            state = 'OFF'
        temperature = pico_temp_sensor.temp
        html = webpage(temperature, state)
        print(client, address)
        client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        client.send(html)
        client.close()


try:
    wlan = connect()
    ip = add_static_if(wlan, LAST_OCTET)
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
