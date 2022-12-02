""" Main script to start up the Pi Pico W, handle wifi and socket, and start second thread for polling the sensor

    Constants are defined here and object instantiated here as well. Could be broken up into some seperate modules to
    provide greater readibility and easier implementation of changes in the future.
 """

import time
from time import sleep
from machine import RTC
import _thread
from hcsr04 import HCSR04
from alarm import Alarm
from lights import PixelStrip
import gc
import socket
import network
import rp2
import network

# Constants
SENSOR_TRIGGER_PIN = 15
SENSOR_ECHO_PIN = 14
ALARM_TRIGGER_PIN = 16
NEOPIXEL_DATA_PIN = 7
NEOPIXEL_NUM_PIXELS = 50
SSID = "WVLKWVY"
PASSWORD = "123456789"
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
HEADER = 64

# Instantiate objects
sensor = HCSR04(trigger_pin = SENSOR_TRIGGER_PIN, echo_pin = SENSOR_ECHO_PIN, echo_timeout_us = 10000)
alarm = Alarm(trigger_pin = ALARM_TRIGGER_PIN)
lights = PixelStrip(data_pin = NEOPIXEL_DATA_PIN, num_pixels = NEOPIXEL_NUM_PIXELS)
rtc = RTC()
connection = 0
lock = _thread.allocate_lock()

def close():
    global running
    
    print("Exiting threads")
    lock.acquire()
    try:
        connection.close()
    except:
        pass
    running = False
    gc.collect()
    print("Done")
    _thread.exit()

# Settings
running = True
wallDistance = 10
alarm_window = (600, 420)

# Second thread that constantly polls the distance of the ultrasonic sensor and acts according to a trigger and settings like alarm_window
def sensorPolling_thread():
    global wallDistance
    global connection
    
    lock.acquire()

    # Wait in case of unstable power during power-up
    sleep(0.1)

    # Calibrate default distance on turn-on
    wallDistance = sensor.distance_cm() - 2
    
    # If return negative value, wall out of range of sensor
    if wallDistance < 0:
        wallDistance = 10
    
    lock.release()
    
    while running:
        lock.acquire()
        
        distance = sensor.distance_cm()
        if (distance > 0) and (distance < wallDistance):
            current_time = rtc.datetime()
            current_time = (current_time[4] * 60) + current_time[5]
            
            if (current_time > alarm_window[0] or current_time < alarm_window[1]) and alarm_window[0] > alarm_window[1]:
                try:
                    connection.sendall("ALARM ACTIVATED  ")
                except Exception as e:
                    pass
                
                alarm.on()
                lights.alarm()
                alarm.off()
            elif (current_time > alarm_window[0] and current_time < alarm_window[1]) and alarm_window[0] < alarm_window[1]:
                try:
                    connection.sendall("ALARM ACTIVATED  ")
                except Exception as e:
                    pass
                
                alarm.on()
                lights.alarm()
                alarm.off()
            else:
                lights.run()
        
        lock.release()
        sleep(.1)

    _thread.exit()

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

        lock.acquire()

        if (message[0] == "COLOR"):
            lights.set_color((int(message[1]), int(message[2]), int(message[3])))
        elif (message[0] == "PRESET"):
            lights.set_preset(int(message[1]))
        elif (message[0] == "ALARM"):
            alarm_window = ((int(message[1][0:2]) * 60 + int(message[1][3:5])), (int(message[2][0:2]) * 60 + int(message[2][3:5])))

        lock.release()

    # Get socket address
    addr = socket.getaddrinfo('0.0.0.0', 5050)[0][-1]

    # Create socket, bind it, and listen for connections
    s = socket.socket()
    #s.setblocking(False)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)

    print('Listening on', addr)
    
    # Start second thread that runs concurrently with the socket receiving below
    _thread.start_new_thread(sensorPolling_thread, ())
    
    # Check for connections and accept them
    while True:
        connected = True

        try:
            connection, addr = s.accept()
            print('Client connected from', addr)
            lock.acquire()
            lights.client_connected()
            lock.release()
            
            while connected:
                msg_length = connection.recv(HEADER).decode(FORMAT) # This allows for variation in input sizes
                if msg_length:
                    msg_length = int(msg_length)
                    msg = connection.recv(msg_length).decode(FORMAT)
                    if msg == DISCONNECT_MESSAGE:
                        connected = False
                    else :
                        handleData(addr, msg)
            print("Client disconnected")
            connection.close()
            
        except OSError as e:
            connection.close()
            print('Connection closed')
            
# Handles closing threads and connections upon exiting the program so threads don't hang or get stuck
except KeyboardInterrupt:
    close()