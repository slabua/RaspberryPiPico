from phew import connect_to_wifi, logging, server
from picozero import pico_temp_sensor, pico_led

SSID = 'YOUR_SSID'
PASSWORD = 'YOUR_PASSWORD'

connect_to_wifi(SSID, PASSWORD)


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


@server.route("/", ["GET"])
def index(request, state='TEST'):
    temperature = pico_temp_sensor.temp
    response = webpage(temperature, state)
    return response


# @server.route("/0", ["GET"])
# def off(request):
#     pico_led.off()
#     return index(request, 'OFF')


# @server.route("/1", ["GET"])
# def on(request):
#     pico_led.on()
#     return index(request, 'ON')


@server.route("/<command>", ["GET"])
def check_state(request, command):
    if '0' in command:
        state = 'OFF'
        pico_led.off()
    elif '1' in command:
        state = 'ON'
        pico_led.on()
    return index(request, state)


@server.catchall()
def my_catchall(request):
    return "No matching route", 404


logging.info("Starting Web Server")
server.run()
