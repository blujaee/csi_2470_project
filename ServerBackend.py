#backend to handle the server side functionality
# note from Maria: wrote more of the server code not sure if it works yet havent tested

import socket
from threading import Thread

from ServersIP import IP

from datetime import date
import signal
import sys
import os


class ServerBackend:
    Clients = []
    UserList = []
    Messages = []

    def __init__(self, HOST, PORT, gui_mode=False, gui_app=None):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gui_mode = gui_mode
        self.gui_app = gui_app
        try:
            self.socket.bind((HOST, PORT))
            self.socket.listen(5)
            self.logMessage('Initiating Chat...')
        except:
            self.logMessage("error: tried running multiple instances of server")
            os._exit(0)

    def logMessage(self, message):
        print(message)
        if self.gui_mode and self.gui_app:
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.gui_app.updateServerLog(message))

    def listen(self):
        while True:
            client_socket, address = self.socket.accept()
            self.logMessage("Received connection with: " + str(address))

            try:
                ClientName = client_socket.recv(1024).decode()
                if not ClientName:
                    self.logMessage("Client disconnected before sending name")
                    client_socket.close()
                    continue

                client = {'ClientName': ClientName, 'client_socket': client_socket, 'address': address}

                self.sendMessage(f"{ClientName} has joined the chat!")

                ServerBackend.UserList.append(ClientName)
                if self.gui_mode:
                    from kivy.clock import Clock
                    Clock.schedule_once(lambda dt: self.gui_app.updateUserList(self.UserList))

                ServerBackend.Clients.append(client)
                Thread(target=self.configureNewClient, args=(client,), daemon=True).start()
            except Exception as e:
                self.logMessage(f"Error receiving client name: {e}")
                client_socket.close()

    def configureNewClient(self, client):
        ClientName = client['ClientName']
        client_socket = client['client_socket']
        while True:
            try:
                clientMessage = client_socket.recv(1024).decode()
                if not clientMessage:
                    break
                ServerBackend.Messages.append(clientMessage)

                if clientMessage.strip() == ClientName + ": bye":
                    self.sendMessage(f"{ClientName} disconnected from chat")
                    break
                else:
                    self.sendMessage(clientMessage)
            except:
                break

        # Clean up after client disconnects
        ServerBackend.Clients.remove(client)
        #ServerBackend.UserList.remove(ClientName)
        client_socket.close()
        if self.gui_mode:
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.gui_app.updateUserList(self.UserList))

    def sendMessage(self, message):
        for client in self.Clients:
            client_socket = client['client_socket']
            try:
                client_socket.send(message.encode())
            except:
                pass 

        self.logMessage(message)

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

    def saveChatRecord(self):
        filename = f"ChatRecord_{date.today()}.txt"
        with open(filename, "w") as f:
            f.write("Users:\n")
            f.write(", ".join(self.UserList) + "\n")
            f.write("Messages:\n")
            f.writelines(message + "\n" for message in self.Messages)
        print(f"Chat record saved to {filename}")

    def SignalHandler(sig, frame):
        print("\nShutting down server...")
        server.shutdown()
        sys.exit(0)


if __name__ == '__main__':
    server = ServerBackend(IP, 3232)

    signal.signal(signal.SIGINT, ServerBackend.SignalHandler)  # Handle Ctrl+C
    server.listen()
       # ServerBackend(IP, 3232) # any socket number 1025 - 65536

