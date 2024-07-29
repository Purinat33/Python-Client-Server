# https://youtu.be/3QiPPX-KeSc?si=uiYJFYU2jQv-_iE3

# This can work even with many clients, even on other PC
# Only works in Local LAN for now.

import socket
import threading  # Multithreading: Per-client basis

####################
# Constant
PORT = 5050  # Pick some empty port
SERVER = "10.0.0.1"
# or
SERVER = socket.gethostbyname(
    socket.gethostname()
)
ADDRESS = (SERVER, PORT)

# Header of len(64) will be sent before any client message to tell us that how much is in the messages
HEADER = 64

# Because sending/receiving everything is in UTF-8
FORMAT = 'utf-8'

# Some sort of way for client to say they're disconnecting
DISCONNECT_MESSAGE = "!DISCONNECT!"

##########################
# Make a socket and open it to connections
server = socket.socket(
    socket.AF_INET,  # Addr type: IPv4 over the internet
    socket.SOCK_STREAM,  # Data type: Stream the data
)

server.bind(ADDRESS)

#########################


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        # Receive message length from the header prepending the message
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)

            # Actual Message
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            # Send something to the client
            conn.send("Message received".encode(FORMAT))

    conn.close()


def start_server():
    server.listen()
    print(f"[Server] Listening on {SERVER}")
    while True:
        # When connection arrives, we store it in an object + address
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"\n[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] Server is starting...")
start_server()
