# backend to support client functionality

import socket
from threading import Thread
import os

from ClientsIP import IP


class ClientBackend:

    def __init__(self, HOST, PORT, gui_mode=False, gui_app=None, username=None):
        self.socket = socket.socket()
        self.gui_mode = gui_mode
        self.gui_app = gui_app
        try:
            self.socket.connect((HOST, PORT))
            if self.gui_mode:
                self.name = username  # Use the username provided by the GUI
            else:
                self.name = input("Enter your name: ")
            self.connectToServer()
        except Exception as e:
            print(f"error: server not running ({e})")
            os._exit(0)

    def connectToServer(self):
        self.socket.send(self.name.encode())
        Thread(target=self.recieveMessage, daemon=True).start()
        if not self.gui_mode:
            self.sendMessageLoop()

    def recieveMessage(self):
        while True:
            try:
                serverMessage = self.socket.recv(1024).decode()
                if not serverMessage.strip():
                    os._exit(0)
                if self.gui_mode:
                    from kivy.clock import Clock
                    Clock.schedule_once(lambda dt: self.gui_app.updateChatHistory(serverMessage))
                else:
                    print(serverMessage)
            except:
                print("error: server unexpectedly shut down")
                os._exit(0)

    def sendMessageLoop(self):
        while True:
            clientInput = input("")
            clientMessage = self.name + ": " + clientInput
            self.socket.send(clientMessage.encode())

    def sendMessage(self, message):
        clientMessage = self.name + ": " + message
        self.socket.send(clientMessage.encode())


if __name__ == '__main__':
        ClientBackend(IP, 3232)
        
    # I think the current bug is because both client and server are waiting for a message that the other isn't sending