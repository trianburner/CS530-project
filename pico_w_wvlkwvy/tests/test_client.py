import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

def send(msg):
    message = msg
    msg_length = len(message)
    send_length = str(msg_length).zfill(HEADER)
    #print(">>" + send_length + message)
    client.send((send_length + message).encode(FORMAT))

def recv():
    msg_in = client.recv(1024).decode(FORMAT)

    return msg_in

def receive(client):
    while True:
        print(client.recv(17).decode(FORMAT), flush = True)

print("Hello Client")
print("------------\n")
print("Type IP of Server")
#SERVER = str(input())
SERVER = "192.168.1.2"
print("------------\n")
print("Connecting...")

ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print("Connected")


print("Enter commands:")
print(f">> To Disconnect, type {DISCONNECT_MESSAGE}")

connected = True
threading.Thread(target=receive, args=[client]).start()
send("COLOR-255-000-000")
send("ALARM-20:00-01:00")
while connected:
    msg_out = str(input())
    if (msg_out):
        print(f"[SENDING MESSAGE] {msg_out}")
        send(msg_out)

    if (msg_out == DISCONNECT_MESSAGE):
        connected = False


client.close()