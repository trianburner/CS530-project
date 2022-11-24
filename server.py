import socket
import threading

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

presetRGB = {"red" : "255000000", 
            "green" : "000255000", 
            "blue" : "000000255", 
            "yellow" : "255255000", 
            "black" : "000000000", 
            "white" : "255255255", 
            "gray" : "128128128", 
            "purple" : "128000128"}


# Parse RGB Values
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

# Handle Client
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            else :
                red, green, blue = ParseRGB(msg)
            print(f"[{addr}] red: {red} green: {green} blue: {blue}")

    conn.close()

# Start
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING} server is starting")
start()
