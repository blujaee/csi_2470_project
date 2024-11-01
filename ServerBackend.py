#backend to handle the server side functionality

import socket
from threading import Thread
import os

from ServersIP import IP

class ServerBackend: # constructor
    Clients = []

    def __init__(self, HOST, PORT):
        return # placeholder to avoid errors
    
def listenForConnections(self):
# listen for requests
    return #another placeholder

def configureNewClient(self, client):
#establish connection with a new client
    return

def sendMessage(self, clientName, message):
# send message prompted by client
    return

if __name__ == 'main':
    #server stuff here
    # may need client IPs here
    ServerBackend(IP, 3232) # any socket number 1025 - 65536