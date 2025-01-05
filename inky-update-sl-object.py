# Connects to the home wifi network, obtains an IP.
# When a button pressed, sends a query string to the endpoint URL
# on an SL object which then changes the texture depending on
# which button is pressed.
# Endpoint URL needs to be updated every time the object is rezzed
# or its script is updated or SL sim server restarted.
# Uses WIFI_CONFIG.py and network_manager.py stored on Pico.
# Can be saved directly on Pico as e.g. main.py

import WIFI_CONFIG
from network_manager import NetworkManager
import time
import uasyncio
import ujson
from urllib import urequest
from machine import Pin
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_INKY_PACK

##############################################################################
# Configure physical inputs/outputs and essential variables                  #
##############################################################################

display = PicoGraphics(display=DISPLAY_INKY_PACK)

# set the screen update speed
# 0 (slowest) to 3 (fastest)
display.set_update_speed(2)

# set the screen font
display.set_font("bitmap8")

button_a = Button(12)
button_b = Button(13)
button_c = Button(14)

led = Pin("LED", Pin.OUT, value=0)

# get the SL objects' endpoint URL by rezzing it / resetting the script
# and appending a query string "?button={0}" to the URL
ENDPOINT = "http://simhost-06d1c22f942641068.agni.secondlife.io:12046/cap/da1bb813-b6c1-f5c6-7cc4-2e619077a520?button={0}";

##############################################################################
# Configure functions                                                        #
##############################################################################

# set white ink (for clearing the screen)
def ink_white():
    display.set_pen(15)

def ink_black():
    display.set_pen(0)

# clear the screen
def clear_screen():
    ink_white()
    display.clear()
    ink_black()

def status_handler(mode, status, ip):
    status_text = "Connecting..."
    if status is not None:
        if status:
            status_text = "Connection successful!"
        else:
            status_text = "Connection failed!"
            clear_screen()
            ink_black()
            display.text("Network: {}".format(WIFI_CONFIG.SSID), 10, 10, scale=2)
            display.text(status_text, 10, 30, scale=2)
            display.text("IP: {}".format(ip), 10, 60, scale=2)
            display.update()
            time.sleep(0.5)

def update_button(network_handle, button):
    # refresh the network connection and re-assign the IP
    uasyncio.get_event_loop().run_until_complete(network_handle.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))

    clear_screen()
    display.text("Button " + button + " pressed", 10, 10, 240, 3)
    display.update()
    time.sleep(0.5)
        
    url = ENDPOINT.format(button)
    print("Requesting URL: {}".format(url))
    response = urequest.urlopen(url)
    response_text = response.read().decode('utf-8')
    response.close()
    print("Server Response: {}".format(response_text))
    status = "UPDATED in SL"
    if response_text != button:
        status = "NOT " + status
        display.text(response_text, 10, 60, scale=2)
    display.text("..." + status, 10, 40, scale=2)
    display.update()
    time.sleep(0.5)

##############################################################################
# Main program                                                               #
##############################################################################

clear_screen()
display.text("Press a button...", 10, 10, 240, 3)
display.update()
        
network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=status_handler)

while True:
    if button_a.read():
        update_button(network_manager, "A")
            
    elif button_b.read():
        update_button(network_manager, "B")
        
    elif button_c.read():
        update_button(network_manager, "C")
        
    time.sleep(0.1)  # this number is how frequently the Pico checks for button presses


