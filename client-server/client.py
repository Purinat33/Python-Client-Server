import socket
import os

from dotenv import load_dotenv
load_dotenv()

####################
# Constant
PORT = 5050  # Pick some empty port
SERVER = os.getenv("SERVER")
# Header of len(64) will be sent before any client message to tell us that how much is in the messages
HEADER = 64
# Because sending/receiving everything is in UTF-8
FORMAT = 'utf-8'
# Some sort of way for client to say they're disconnecting
DISCONNECT_MESSAGE = "!DISCONNECT!"
ADDRESS = (SERVER, PORT)
##########################

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

# Connect to the server
client.connect(ADDRESS)  # Not bind this time


def send(msg: str):
    message = msg.encode(FORMAT)  # We need to send in Bytes not String
    # We also need the length to be sent as header
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)

    # Pad send_length until its 64 Bytes long for header
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(128))


message = input("Input Text: ")
send(message)
# send("Hello World!")
# send("Welcome!")
send("!DISCONNECT!")
