import machine
import utime				# utime is used with microcontrollers
                            # if time is used, utime will be used, instead
import _thread

led_pedestrian = machine.Pin("LED", machine.Pin.OUT)
led_red = machine.Pin(15, machine.Pin.OUT)
led_amber = machine.Pin(14, machine.Pin.OUT)
led_green = machine.Pin(13, machine.Pin.OUT)
button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
buzzer = machine.Pin(12, machine.Pin.OUT)

global button_pressed
button_pressed = False

def button_reader_thread():
    global button_pressed
    while True:
        if button.value() == 1:
            button_pressed = True
            
_thread.start_new_thread(button_reader_thread, ())

while True:
    if button_pressed == True:
        led_red.value(1)
        led_pedestrian.value(1)
        for i in range(10):
            buzzer.value(1)
            utime.sleep(0.2)
            buzzer.value(0)
            utime.sleep(0.2)
        global button_pressed
        led_pedestrian.value(0)
        button_pressed = False
    led_red.value(1)
    utime.sleep(10)
    led_amber.value(1)
    utime.sleep(3)
    led_red.value(0)
    led_amber.value(0)
    led_green.value(1)
    utime.sleep(10)
    led_green.value(0)
    led_amber.value(1)	# or led_amber.on()
    utime.sleep(2)
    led_amber.value(0)	# or led_amber.off()

