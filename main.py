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
alarm_window = (1230, 420)

cl = 0

def sensorPolling_thread():
    global wallDistance
    global cl
    
    while running:
        distance = sensor.distance_cm()
        if (distance > 0) and (distance < wallDistance) :
            current_time = rtc.datetime()
            current_time = (current_time[4] * 60) + current_time[5]
            
            if current_time > alarm_window[0] or current_time < alarm_window[1]:
                try:
                    cl.send("ALARM ACTIVATED  ")
                except:
                    pass
                
                alarm.on()
                lights.run(2)
                alarm.off()
            else:
                try:
                    cl.send("MOVEMENT DETECTED")
                except:
                    pass
                
                lights.run(1)
        else:
            pass
        sleep(.1)

    _thread.exit()

_thread.start_new_thread(sensorPolling_thread, ())

try:
    # Configure AP settings
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=SSID, password=PASSWORD)
    ap.active(True)

    # Wait until the AP is active until continuing
    while ap.active == False:
        pass

    # Disable power-saving
    ap.config(pm = 0xa11140)
    
    # Set static IP address
    ap.ifconfig(('192.168.1.2', '255.255.255.0', '192.168.1.1', '8.8.8.8'))
    
    # Set country
    rp2.country('US')

    print("Access point active")
    print(ap.ifconfig())
    

    # See the MAC address in the wireless chip OTP
    #mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    #print('mac = ' + mac)
        
    # Get socket address
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    # Create socket, bind it, and listen for connections
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)

    print('Listening on', addr)
    
    # Check for connections and accept them
    while True:
        try:
            cl, addr = s.accept()
            print('Client connected from', addr)
            
            while True:
                r = cl.recv(1024)
                print(r)
            
        except OSError as e:
            cl.close()
            print('Connection closed')
            
except KeyboardInterrupt:
    running = False
    print("Exiting threads")
    time.sleep(10)
    gc.collect()
    print("Done")
    _thread.exit()