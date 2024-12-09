#backend to handle the server side functionality

import socket
from threading import Thread

from ServersIP import IP

from datetime import date
import signal
import sys
import os


class ServerBackend:
    # initialize LISTS (shared variables) to store information
    Clients = []
    #These lists are used to keep track of all chat users and the messages sent
    UserList = [] 
    Messages = []

    # Constructor METHOD to initialize an instance of ServerBackend
    def __init__(self, HOST, PORT, gui_mode=False, gui_app=None):
        # Initialize server's socket for connection
        # self.socket creates an instance of the socket CLASS
        # AKA it creates a TCP socket OBJECT
        # AF_INET refers to IPv4 and SOCK_STREAM refers to TCP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Instance attributes to 
        self.gui_mode = gui_mode
        self.gui_app = gui_app
        try:
            # Calls .bind() METHOD to bind host and port
            self.socket.bind((HOST, PORT))
            # Calls .listen() METHOD to start listening for clients
            # argument '5' means only 5 clients can join
            self.socket.listen(5)
            # calls logMessage METHOD
            self.logMessage('Initiating Chat...')
        except:
            # If bind doesn't work, call logMessage METHOD and write error message
            self.logMessage("error: tried running multiple instances of server")
            # Calls function to exit
            os._exit(0)

    # METHOD logMessage logs a message to the console and updates the GUI
    def logMessage(self, message):
        # Print message to console
        print(message)
        # If in GUI mode, update the GUI's server log using Kivy Clock
        if self.gui_mode and self.gui_app:
            # importing Clock here means that it is only imported if needed
            from kivy.clock import Clock
            # Calls Clock METHOD from Kivy to schedule updates on a background thread
            # This means the GUI is updated 
            # dt is the time that has passed since the last frame
            # A lambda is an ANONYMOUS FUNCTION 
            Clock.schedule_once(lambda dt: self.gui_app.updateServerLog(message))

    # Method to listen for new client connections\
    # defines METHOD listen()
    def listen(self):
        while True:
            # accepts new client connection
            client_socket, address = self.socket.accept()
            # calls logMessage method
            self.logMessage("Received connection with: " + str(address))

            try:
                ClientName = client_socket.recv(1024).decode()
                if not ClientName:
                    # if ClientName isnt sent, log an error message and close the connection
                    self.logMessage("Client disconnected before sending name")
                    client_socket.close()
                    continue
                
                # Creates new DICTIONARY to represent the client
                client = {'ClientName': ClientName, 'client_socket': client_socket, 'address': address}

                # Calls sendMessage method to notift other clients that a new client has joined the class
                self.sendMessage(f"{ClientName} has joined the chat!")
                # calls ServerBackend CLASS and .append() METHOD to add ClientName to UserList
                ServerBackend.UserList.append(ClientName)
                if self.gui_mode:
                    # Calls Clock METHOD from Kivy to schedule updates on a background thread
                    # This means the GUI is updated 
                    # dt is the time that has passed since the last frame
                    # A lambda is an ANONYMOUS FUNCTION
                    from kivy.clock import Clock
                    Clock.schedule_once(lambda dt: self.gui_app.updateUserList(self.UserList))

                # calls ServerBackend CLASS and .append() METHOD to add new client to Clients LIST 
                ServerBackend.Clients.append(client)
                # calls Thread CLASS to instantiate another class to handle the new client
                Thread(target=self.configureNewClient, args=(client,), daemon=True).start()
            except Exception as e:
                self.logMessage(f"Error receiving client name: {e}")
                client_socket.close()

    # defines configureNewClient METHOD to communicate with specific clients
    # self and client are both ARGUMENTS of the METHOD
    def configureNewClient(self, client):
        # Extract client details from the dictionary
        ClientName = client['ClientName']
        client_socket = client['client_socket']
        while True:
            try:
                # recieve a message from the client
                # .recv() is a METHOD of the socket OBJECT
                # 1024 is the buffer size
                # uses .decode() method to convert the byte data into a string
                clientMessage = client_socket.recv(1024).decode()

                if not clientMessage:
                    break
                # calls .append() METHOD to add the message to the Messages LIST in ServerBackend CLASS
                ServerBackend.Messages.append(clientMessage)

                # if client sends "bye" they are disconnected from the chat
                if clientMessage.strip() == ClientName + ": bye":
                    # calls sendMessage METHOD
                    self.sendMessage(f"{ClientName} disconnected from chat")
                    break
                else:
                    # if the client didn't send bye, send their message usinf sendMessage METHOD
                    self.sendMessage(clientMessage)
            except:
                break

        # Clean up after client disconnects, this affects ServerGUI
        # calls .remove() METHOD to remove the client information from the Clients LIST in ServerBackend CLASS
        ServerBackend.Clients.remove(client)
        # calls .close() METHOD to close that clients socket
        client_socket.close()

        # Uses Kivy clock to update the UserList in the GUI
        if self.gui_mode:
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.gui_app.updateUserList(self.UserList))

    # defines sendMessage METHOD
    def sendMessage(self, message):
        for client in self.Clients:
            client_socket = client['client_socket']
            try:
                client_socket.send(message.encode())
            except:
                pass 

        self.logMessage(message)
    #sets up safe server closure to allow for txt file to be finalized and saved
    def shutdown(self):
        self.is_running = False
        # Close all client connections
        for client in self.Clients:
            try:
                client['client_socket'].close()
            except Exception:
                pass
        self.socket.close()
        self.saveChatRecord()
    #writes a txt file displaying all clients that joined the server and the messages that they sent
    #saves with current date using 'date.today()'
    def saveChatRecord(self):
        filename = f"ChatRecord_{date.today()}.txt"
        with open(filename, "w") as f:
            f.write("Users:\n")
            f.write(", ".join(self.UserList) + "\n") #prints all users in one line
            f.write("Messages:\n")
            f.writelines(message + "\n" for message in self.Messages) #separates messages into different lines
        print(f"Chat record saved to {filename}")
    #shuts down server and displays that action being done on the terminal
    def SignalHandler(sig, frame):
        print("\nShutting down server...")
        server.shutdown()
        sys.exit(0)


if __name__ == '__main__':
    server = ServerBackend(IP, 3232)

    signal.signal(signal.SIGINT, ServerBackend.SignalHandler)  # Handle Ctrl+C
    server.listen()

