import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class ClientGUI(ServerClientGUI):
        def __init__(self, client_backend, **kwargs):
            super().__init__(**kwargs)
            self.orientation = "vertical"
            self.client_backend = client_backend
    
#to display chat
        self.chat_display = Label(size_hint_y=None, height=500, text="", valign="top", halign="left")
        self.chat_display.bind(size=self.update_chat_size)
        scroll_view = ScrollView(size_hint=(1, None), size=(self.width, 500))
        scroll_view.add_widget(self.chat_display)
        self.add_widget(scroll_view)

        self.input_field = TextInput(size_hint_y=None, height=40, multiline=False, hint_text="Type a message")
        self.add_widget(self.input_field)

        self.send_button = Button(text="Send", size_hint_y=None, height=40)
        self.send_button.bind(on_press=self.send_message)
        self.add_widget(self.send_button)

# Input field for typing messages
        self.input_field = TextInput(size_hint_y=None, height=40, multiline=False, hint_text="Type a message")
        self.add_widget(self.input_field)

# Send button
        self.send_button = Button(text="Send", size_hint_y=None, height=40)
        self.send_button.bind(on_press=self.send_message)
        self.add_widget(self.send_button)def update_chat_size(self, *args):
        """Ensure the chat display updates dynamically as messages are added."""
        self.chat_display.text_size = (self.chat_display.width, None)
        self.chat_display.height = self.chat_display.texture_size[1]

    def update_chat_display(self, message):
        self.chat_display.text += f"{message}\n"

    def send_message(self, *args):
        message = self.input_field.text
        if message.strip():
# Send the message with the backend's socket
            self.client_backend.socket.send((self.client_backend.name + ": " + message).encode())
            self.input_field.text = ""  # Clear the input field

def loadClientElements(client_backend):
    return ClientGUI(client_backend)

class ClientApp(App):
    def __init__(self, client_backend, **kwargs):
        super().__init__(**kwargs)
        self.client_backend = client_backend  # Pass backend to the app

    def build(self):
#buikd and run GUI
        return loadClientElements(self.client_backend)

if __name__ == "__main__":
    # Prompt for IP and PORT
    HOST = input("Enter the server's IP address (default is 127.0.0.1): ") or "127.0.0.1"
    PORT = input("Enter the server's port (default is 3232): ")
    PORT = int(PORT) if PORT else 3232

# Start the backend from ClientBackend.py
    from ClientBackend import ClientBackend
    client_backend = ClientBackend(HOST, PORT)

# Start the GUI
    ClientApp(client_backend).run()
    
    
def loadClientElements():
    return
