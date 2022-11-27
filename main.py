import time
from time import sleep
from machine import Pin
from machine import RTC
import utime
import _thread
from hcsr04 import HCSR04
from alarm import Alarm
from lights import PixelStrip
import gc
import socket
import network
import rp2
import network
import ubinascii
import urequests as requests

# Constants
SENSOR_TRIGGER_PIN = 15
SENSOR_ECHO_PIN = 14
ALARM_TRIGGER_PIN = 13
NEOPIXEL_DATA_PIN = 7
NEOPIXEL_NUM_PIXELS = 50
SSID = "Wlkway LED Controller"
PASSWORD = "123456789"

# Instantiate objects
sensor = HCSR04(trigger_pin = SENSOR_TRIGGER_PIN, echo_pin = SENSOR_ECHO_PIN, echo_timeout_us = 10000)
alarm = Alarm(trigger_pin = ALARM_TRIGGER_PIN)
lights = PixelStrip(data_pin = NEOPIXEL_DATA_PIN, num_pixels = NEOPIXEL_NUM_PIXELS)
rtc = RTC()

# Settings
running = True
wallDistance = 10
alarm_window = (20, 30, 07, 00)

def sensorPolling_thread():
    global wallDistance
    global running
    global sensor
    global alarm
    global lights
    global alarm_window
    
    while running:
        distance = sensor.distance_cm()
        if (distance > 0) and (distance < wallDistance) :
            alarm.on()
            lights.run()
            alarm.off()
        else:
            pass
        sleep(.1)

    _thread.exit()

_thread.start_new_thread(sensorPolling_thread, ())

try:
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=SSID, password=PASSWORD) 
    ap.active(True)

    while ap.active == False:
        pass

    ap.ifconfig(('192.168.1.2', '255.255.255.0', '192.168.1.1', '8.8.8.8'))

    print("Access point active")
    print(ap.ifconfig())
    
    # Set country to avoid possible errors
    rp2.country('US')


    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # Disable power-saving
    wlan.config(pm = 0xa11140)

    # See the MAC address in the wireless chip OTP
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print('mac = ' + mac)
        
    # HTTP server with socket
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)

    print('Listening on', addr)
    # Listen for connections
    while True:
        try:
            cl, addr = s.accept()
            print('Client connected from', addr)
            r = cl.recv(1024)
            # print(r)
            
            r = str(r)
                
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')

            cl.close()
            
        except OSError as e:
            cl.close()
            print('Connection closed')
            
except KeyboardInterrupt:
    running = False
    time.sleep(10)
    gc.collect()
    sys.exit()