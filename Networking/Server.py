"""
Server.py implements all functions for receiving & parsing data from App
"""

import threading
from System import Internal
from ServerOverhead import HEADER, SERVER, FORMAT, DISCONNECT_MESSAGE

# handleData() determines whether device's LED color or alarm window is being updated
def handleData(addr, msg):
    """
    determines whether device's LED color or alarm window is being updated
    :param addr: current conn's ip
    :param msg: msg from conn
    """
    message = msg.split("-")
    print(f"[{addr}]: ${msg}")

    if (message[0] == "COLOR"):
        Internal.changeRGB([message[1], message[2], message[3]])
    elif (message[0] == "ALARM"):
        Internal.changeAlarmStart(message[1])
        Internal.changeAlarmEnd(message[2])

def handleClient(conn, addr):
    """
    receives a connection and grabs transferred strings, grabs first HEADER to determine string length
    :param conn: current conn
    :param addr: conn ip
    """
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # This allows for variation in input sizes
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            else :
                handleData(addr, msg)
    conn.close()

def start(server):
    """
    begins listening, can handle multiple clients
    :param server: active Socket
    """
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
