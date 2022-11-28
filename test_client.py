import socket
import threading

HEADER = 64
PORT = 80
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def recv():
    msg_in = client.recv(1024).decode(FORMAT)

    return msg_in

def receive(client):
    while True:
        print(client.recv(17).decode(FORMAT), flush = True)

print("Hello Client")
print("------------\n")
print("Type IP of Server")
SERVER = str(input())

ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

print("------------\n")
print("What Color Would You Like?")
print(f">> To Disconnect, type {DISCONNECT_MESSAGE}")

connected = True
threading.Thread(target=receive, args=[client]).start()
while connected:
    msg_out = str(input())
    if (msg_out):
        print(f"[SENDING MESSAGE] {msg_out}")
        send(msg_out)

    if (msg_out == DISCONNECT_MESSAGE):
        connected = False


client.close()