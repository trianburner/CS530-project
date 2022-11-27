import socket
import threading
from lights import PixelStrip
from alarm import Alarm
from main import sensorPolling_thread

NEOPIXEL_DATA_PIN = 7
NEOPIXEL_NUM_PIXELS = 50
ALARM_TRIGGER_PIN = 13

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# Create Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind Socket
server.bind(ADDR)

lights = PixelStrip(data_pin = NEOPIXEL_DATA_PIN, num_pixels = NEOPIXEL_NUM_PIXELS)
alarm = Alarm(trigger_pin = ALARM_TRIGGER_PIN)
alarm_window = sensorPolling_thread.alarm_window

presetRGB = {"red" : "255000000", 
            "green" : "000255000", 
            "blue" : "000000255", 
            "yellow" : "255255000", 
            "black" : "000000000", 
            "white" : "255255255", 
            "gray" : "128128128", 
            "purple" : "128000128"}


# Parse RGB Values
# This is just sitting here.
def ParseRGB(msg) :
    if msg in presetRGB:
        value = presetRGB[msg]
        red = int(value[0:3])
        green = int(value[3:6])
        blue = int(value[6:9])
    else :
        red = int(msg[0:3])
        green = int(msg[3:6])
        blue = int(msg[6:9])

    return red, green, blue

# I ultimately don't know where any of this info is going.
def Begin(conn, addr, msg):
    message = msg.split("-")
    if (message[0] == "COLOR"):
        print(f"[{addr}] COLOR")
        lights.run(0,(message[1],message[2],message[3]))
        # lights.alt_color
    elif (message[0] == "ALARM"):
        print(f"[{addr}] ALARM")
        alarm_window = (message[1], message[2])
        # alarm.on()
    elif (message[0] == "POWER"):
        print(f"[{addr}] POWER")
        pass
    

# Handle Client

# sends and recieves are sequential. Once it is in a receive state, it will not move on till the socket receives a message
def recv(conn, addr):
    print(f"[NEW CONNECTION] {addr} ready to receive")
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # This allows for variation in input sizes
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            else :
                send(conn,addr,"Instruction Recieved")
                Begin(conn, addr, msg)

    conn.close()

def send(conn, addr, msg):
    
    conn.send(msg.encode(FORMAT))

    print("[STATUS] message sent to {addr}")

# Start
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        recv_thread = threading.Thread(target=recv, args=(conn,addr))
        recv_thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING} server is starting")
start()
