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
        self.socket.send(self.name.encode()) # send name down the socket once the user has input it
        Thread(target=self.recieveMessage, daemon=True).start() # start listening for messages
        if not self.gui_mode: # if the GUI isn't active, can still run in terminal via a different method
            self.sendMessageLoop()

    def recieveMessage(self):
        while True: #always listen for messages
            try:
                serverMessage = self.socket.recv(1024).decode() #recieve message on the socket
                if not serverMessage.strip(): # if server couldn't be connected to
                    os._exit(0)
                if self.gui_mode:
                    from kivy.clock import Clock
                    Clock.schedule_once(lambda dt: self.gui_app.updateChatHistory(serverMessage))
                else:
                    print(serverMessage)
            except:
                print("error: server unexpectedly shut down")
                os._exit(0)

    def sendMessageLoop(self): # if GUI is not active
        while True:  #always wait for input to send message
            clientInput = input("") # input = what client types
            clientMessage = self.name + ": " + clientInput
            self.socket.send(clientMessage.encode())

    def sendMessage(self, message): # if GUI is active
        clientMessage = self.name + ": " + message
        self.socket.send(clientMessage.encode())


if __name__ == '__main__': # to run main
        ClientBackend(IP, 3232)  # create instance of client - now in clientGUI