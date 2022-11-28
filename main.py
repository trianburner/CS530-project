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
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
HEADER = 64

# Instantiate objects
sensor = HCSR04(trigger_pin = SENSOR_TRIGGER_PIN, echo_pin = SENSOR_ECHO_PIN, echo_timeout_us = 10000)
alarm = Alarm(trigger_pin = ALARM_TRIGGER_PIN)
lights = PixelStrip(data_pin = NEOPIXEL_DATA_PIN, num_pixels = NEOPIXEL_NUM_PIXELS)
rtc = RTC()
cl = 0

# Settings
running = True
pause = False
wallDistance = 10
alarm_window = (1230, 420)

def sensorPolling_thread():
    global wallDistance
    global cl
    
    wallDistance = sensor.distance_cm() - 2
    
    if wallDistance < 0:
        wallDistance = 10
    
    while running:
        
        distance = sensor.distance_cm()
        if (distance > 0) and (distance < wallDistance) and not pause:
            current_time = rtc.datetime()
            current_time = (current_time[4] * 60) + current_time[5]
            
            if (current_time > alarm_window[0] or current_time < alarm_window[1]) and alarm_window[0] > alarm_window[1]:
                try:
                    cl.sendall("ALARM ACTIVATED  ")
                except Exception as e:
                    pass
                
                alarm.on()
                lights.run(2)
                alarm.off()
            elif (current_time > alarm_window[0] and current_time < alarm_window[1]) and alarm_window[0] < alarm_window[1]:
                try:
                    cl.sendall("ALARM ACTIVATED  ")
                except Exception as e:
                    pass
                
                alarm.on()
                lights.run(2)
                alarm.off()
            else:
                
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
    
    def handleData(addr, msg):
        """
        determines whether device's LED color or alarm window is being updated
        :param addr: current conn's ip
        :param msg: msg from conn
        """
        
        global alarm_window
        
        message = msg.split("-")
        print(f"[{addr}]: ${msg}")

        if (message[0] == "COLOR"):
            lights.run(0, (int(message[1]), int(message[2]), int(message[3])))
        elif (message[0] == "ALARM"):
            alarm_window = ((int(message[1][0:2]) * 60 + int(message[1][3:5])), (int(message[2][0:2]) * 60 + int(message[2][3:5])))

    # Get socket address
    addr = socket.getaddrinfo('0.0.0.0', 5050)[0][-1]

    # Create socket, bind it, and listen for connections
    s = socket.socket()
    #s.setblocking(False)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)

    print('Listening on', addr)
    
    # Check for connections and accept them
    while True:
        connected = True
    
        
        try:
            cl, addr = s.accept()
            lights.run(1)
            print('Client connected from', addr)
            
            while connected:
                msg_length = cl.recv(HEADER).decode(FORMAT) # This allows for variation in input sizes
                if msg_length:
                    msg_length = int(msg_length)
                    msg = cl.recv(msg_length).decode(FORMAT)
                    if msg == DISCONNECT_MESSAGE:
                        connected = False
                    else :
                        handleData(addr, msg)
            print("Client disconnected")
            cl.close()
            
        except OSError as e:
            cl.close()
            print('Connection closed')
            
except KeyboardInterrupt:
    #cl.close()
    running = False
    print("Exiting threads")
    time.sleep(10)
    gc.collect()
    print("Done")
    _thread.exit()