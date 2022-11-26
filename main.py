import time
from time import sleep
from machine import Pin
import utime
import _thread
from hcsr04 import HCSR04
from alarm import Alarm
from lights import PixelStrip
import socket
import network
import rp2
import network
import ubinascii
import urequests as requests

# Pin setting constants
SENSOR_TRIGGER_PIN = 15
SENSOR_ECHO_PIN = 14
ALARM_TRIGGER_PIN = 13
NEOPIXEL_DATA_PIN = 7
NEOPIXEL_NUM_PIXELS = 50

# Instantiate objects
sensor = HCSR04(trigger_pin = SENSOR_TRIGGER_PIN, echo_pin = SENSOR_ECHO_PIN, echo_timeout_us = 10000)
alarm = Alarm(trigger_pin = ALARM_TRIGGER_PIN)
lights = PixelStrip(data_pin = NEOPIXEL_DATA_PIN, num_pixels = NEOPIXEL_NUM_PIXELS)
LED = machine.Pin("LED", machine.Pin.OUT)

# Settings
running = True
wallDistance = 10
color = (255, 0, 0)
preset = 0
alarmOn = False

def sensorPolling_thread():
    global wallDistance
    global color
    global preset
    global alarmOn
    
    while running:
        distance = sensor.distance_cm()
        #print('Distance:', distance, 'cm')
        if (distance > 0) and (distance < wallDistance) :
            alarm.on()
            lights.rainbow_cycle()
        else:
            alarm.off()
        sleep(.1)
    
    alarm.off()
    lights.fadeOff()
    _thread.exit()

_thread.start_new_thread(sensorPolling_thread, ())

try:
    ssid = "Wlkway LED Controller"
    password = "123456789"

    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password) 
    ap.active(True)

    while ap.active == False:
        pass

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

    # Wait for connection with 10 second timeout
    timeout = 10
    while timeout > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        timeout -= 1
        print('Waiting for connection...')
        time.sleep(1)

    status = wlan.ifconfig()
    print('ip = ' + status[0])
        
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
            
            html_name = 'index.html'
            file = open(html_name, 'r')
            while True:
                # Read the next 1KB chunk
                chunk = file.read(1024)
                if not chunk:
                    break
                # Send the next 1 KB chunk
                cl.send(chunk)
            
            cl.close()
            file.close()
            
        except OSError as e:
            cl.close()
            print('Connection closed')
except KeyboardInterrupt:
    running = False
    _thread.exit()