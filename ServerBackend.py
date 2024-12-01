#backend to handle the server side functionality
# note from Maria: wrote more of the server code not sure if it works yet havent tested
import socket
from threading import Thread

from ServersIP import IP

from datetime import date
import signal
import sys

class ServerBackend: # constructor
    Clients = []
    UserList = [] #delete if causes issues -Maria
    Messages = [] #delete if causes issues -Maria
    

    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen(5)
        print('Initiating Chat...')
    
    def listen(self):
        while True:
            client_socket, address = self.socket.accept()
            print("Recieved connection with:" + str(address)) # this prints

            ClientName = client_socket.recv(1024).decode()
            client = {'ClientName': ClientName, 'client_socket': client_socket}

            self.sendMessage(ClientName, "Say hi to " + ClientName + "!")

            ServerBackend.UserList.append(ClientName) #delete if causes issues -Maria

            ServerBackend.Clients.append(client)
            Thread(target=self.configureNewClient, args=(client,)).start()

    def configureNewClient(self, client):
        ClientName = client['ClientName']
        client_socket = client['client_socket']
        while True:  # Get stuck here where client cannot send a message - can't type in terminal
            clientMessage = client_socket.recv(1024).decode()
            ServerBackend.Messages.append(clientMessage) #note delete if causes issues - Maria

            if clientMessage.strip() == ClientName + ": bye" or not clientMessage.strip():
                self.sendMessage(ClientName, ClientName + " disconnected from chat")
                ServerBackend.Clients.remove(client)
                client_socket.close()

                break
            else:
                self.sendMessage(ClientName, clientMessage)
    #establish connection with a new client


    def sendMessage(self, clientSending, message):
        for client in self.Clients:
            client_socket = client['client_socket']
            ClientName = client['ClientName']
            if ClientName != clientSending:
                client_socket.send(message.encode())
    # send message prompted by client

    #delete if causes issues -Maria
    def shutdown(self):
        self.is_running = False
        # Close all client connections
        for client in self.Clients:
            try:
                client['client_socket'].close()
            except Exception:
                pass
        self.socket.close()
        self.save_chat_record()
    #delete if causes issues -Maria
    def save_chat_record(self):
        filename = f"ChatRecord_{date.today()}.txt"
        with open(filename, "w") as f:
            f.write("Users:\n")
            f.write(", ".join(self.UserList) + "\n")
            f.write("Messages:\n")
            f.writelines(message + "\n" for message in self.Messages)
        print(f"Chat record saved to {filename}")
   

   #delete if causes issues -Maria
    def SignalHandler(sig, frame):
        print("\nShutting down server...")
        server.shutdown()
        sys.exit(0)




if __name__ == '__main__':
    server = ServerBackend(IP, 3232)

    signal.signal(signal.SIGINT, ServerBackend.SignalHandler)  # Handle Ctrl+C delete if causes issues -Maria
    server.listen()
   # ServerBackend(IP, 3232) # any socket number 1025 - 65536

    
   #message saving will delete if doesnt work -Maria
    f = open("ChatRecord" + str(date.today()), "a")

    f.write("Users:")

    for i in UserList:
        f.write(str(i) + ", ")

    for x in Messages:
        f.write(str(x)+ "\n")
    f.close()


