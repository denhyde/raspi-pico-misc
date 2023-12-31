# Uses WIFI_CONFIG.py
# stored on Pico

# Example Led on/ Led off program from raspberry pi foundation for Pico W that has been updated to show ip address on inky pack

import network
import WIFI_CONFIG
import time
import socket

from machine import Pin
import uasyncio as asyncio

from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_INKY_PACK

display = PicoGraphics(display=DISPLAY_INKY_PACK)

# you can change the update speed here!
# it goes from 0 (slowest) to 3 (fastest)
display.set_update_speed(2)

display.set_font("bitmap8")

button_a = Button(12)  #Buttons not used in this but named incase you want to use them.
button_b = Button(13)
button_c = Button(14)


# a handy function we can call to clear the screen
# display.set_pen(15) is white and display.set_pen(0) is black
def clear():
    display.set_pen(15)
    display.clear()

led = Pin("LED", Pin.OUT, value=0)

ssid = WIFI_CONFIG.SSID
password = WIFI_CONFIG.PSK

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html = """<!DOCTYPE html>
<html>
    <head> <title>Pico W</title> </head>
    <body> <h1>Pico W</h1>
        <p>%s</p>
    </body>
</html>
"""

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    clear()
    display.set_pen(0)
    display.text("Waiting for Connection", 10, 10, 240, 3)
    display.update()
    time.sleep(0.5)
    time.sleep(1)

if wlan.status() != 3:
    clear()
    display.set_pen(0)
    display.text("Network Connection Failed", 10, 10, 240, 3)
    display.update()
    time.sleep(0.5)
    raise RuntimeError('network connection failed')

else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    clear()
    display.set_pen(0)
    display.text("IP = ", 10, 10, 240, 3)
    display.text(status[0], 10,50,240,3)
    display.text("Connected", 10,90,240,3)
    display.update()
    time.sleep(0.5)

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)
stateis = ""
print('listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)

        request = str(request)
        led_on = request.find('/light/on')
        led_off = request.find('/light/off')
        print( 'led on = ' + str(led_on))
        print( 'led off = ' + str(led_off))

        if led_on == 6:
            print("led on")
            led.value(1)
            stateis = "LED is ON"
            clear()
            display.set_pen(0)
            display.text("IP = ", 10, 10, 240, 3)
            display.text(status[0], 10,50,240,3)
            display.text("LED is ON", 10,90,240,3)
            display.update()
            time.sleep(0.5)

        if led_off == 6:
            print("led off")
            led.value(0)
            stateis = "LED is OFF"
            clear()
            display.set_pen(0)
            display.text("IP = ", 10, 10, 240, 3)
            display.text(status[0], 10,50,240,3)
            display.text("LED is OFF", 10,90,240,3)
            display.update()
            time.sleep(0.5)            
            

        response = html % stateis

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')
