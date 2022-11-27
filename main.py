import threading
import time
from Networking.ServerOverhead import ADDR
import _thread
import gc
import socket
import rp2
import network
from Networking.Server import start
from Management.MotionDetection import pollSensor

def configureAP():
    """
    sets up an access point for the LED Device
    """
    SSID = "Wlkway LED Controller"
    PASSWORD = "123456789"

    ap = network.WLAN(network.AP_IF)
    ap.config(essid=SSID, password=PASSWORD)
    ap.active(True)

    # Wait until the AP is active until continuing
    while ap.active == False:
        pass

    # Disable power-saving
    ap.config(pm=0xa11140)

    # Set static IP address
    ap.ifconfig(('192.168.1.2', '255.255.255.0', '192.168.1.1', '8.8.8.8'))

    # Set country
    rp2.country('US')

"""
Program's start
"""
try:
    # Configure AP settings
    configureAP()

    # Create socket, bind it
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    # Multithreading - Both listens for connections & checks sensor for motion
    threading.Thread(target=pollSensor, args=[server])
    threading.Thread(target=start, args=[server])
            
except KeyboardInterrupt:
    running = False
    print("Exiting threads")
    time.sleep(10)
    gc.collect()
    print("Done")
    _thread.exit()