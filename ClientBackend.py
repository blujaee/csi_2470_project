# backend to support client functionality

import socket
from threading import Thread
import os

from ClientsIP import IP

class ClientBackend:

    def __init__(self, HOST, PORT):
        self.socket = socket.socket()
        self.socket.connect((HOST, PORT))
        self.name = input("Enter your name: ")

        connectToServer(self)

def connectToServer(self):
    self.socket.send(self.name.encode())
    Thread(target = recieveMessage(self)).start()  # is waiting for a message from server?
    print("send message")
    sendMessage(self)
    
def recieveMessage(self):
    while True:
        serverMessage = self.socket.recv(3232).decode()
        if not serverMessage.strip():
            os._exit(0)


def sendMessage(self):
    while True:
        clientInput = input("Send Message: ")
        clientMessage = self.name + ": " + clientInput
        self.socket.send(clientMessage.encode())
    
if __name__ == '__main__':
    ClientBackend(IP, 3232)

    # I think the current bug is because both client and server are waiting for a message that the other isn't sending