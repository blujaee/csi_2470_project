#backend to handle the server side functionality
# note from Maria: wrote more of the server code not sure if it works yet havent tested
import socket
from threading import Thread
import os

from ServersIP import IP

class ServerBackend: # constructor
    Clients = []

    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen(5)
        print('Initiating Chat...')
        #return # placeholder to avoid errors
    
def listenForConnections(self):
    while True:
        client_socket, adress = self.socket.accept()
        print("Recieved connection with:" + str(adress))

        ClientName = client_socket.recv(1024).decode()
        client = {'ClientName': ClientName, 'client_socket': client_socket}

        self.broadcast_message(ClientName, "Say hi to" + ClientName + "!")

        Server.Clients.append(client)
        Thread(target = configureNewClient, args = (client,)).start()
# listen for requests
    #return #another placeholder

def configureNewClient(self, client):
    ClientName = client['client_name']
    client_socket = client['client_socket']
    while True:
        clientMessage = client_socket.recv(1024).decode()

        if client_message.strip() == ClientName + ": bye" or not clientMessage.strip():
            self.sendMessage(ClientName, ClientName + "disconnected from chat")
            Server.clients.remove(client)
            client_socket.close()
            break
        else:
            self.sendMessage(ClientName, clientMessage)
#establish connection with a new client
    return

def sendMessage(self, clientSending, message):
    for client in self.Clients:
        client_socket = client['client_socket']
        ClientName = client['ClientName']
        if ClientName != clientSending:
            client_socket.send(message.encode())
# send message prompted by client
    return

if __name__ == 'main':
    #server = Server('127.0.0.1' 7632)
    #server.listen()
    #server stuff here
    # may need client IPs here
    ServerBackend(IP, 3232) # any socket number 1025 - 65536