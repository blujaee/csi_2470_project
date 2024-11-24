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

        self.connectToServer()

    def connectToServer(self):
        self.socket.send(self.name.encode())
        Thread(target = self.recieveMessage).start()  
        self.sendMessage()
        
    def recieveMessage(self):
        while True:
            serverMessage = self.socket.recv(1024).decode()
            if not serverMessage.strip():
                os._exit(0)
            print(serverMessage)


    def sendMessage(self):
        while True:
            clientInput = input("")
            clientMessage = self.name + ": " + clientInput
            self.socket.send(clientMessage.encode())
    
if __name__ == '__main__':
    ClientBackend(IP, 3232)

    # I think the current bug is because both client and server are waiting for a message that the other isn't sending