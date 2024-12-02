from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from threading import Thread
import socket
import os

from ClientsIP import IP
from ClientBackend import ClientBackend


class ChatClientApp(App):
    def build(self):
        self.title = "Chat Client"

        # Initialize the root widget
        self.root = BoxLayout()

        # Before building the chat interface, prompt for user name
        self.username = ''
        self.showUsernamePopup()

        return self.root  # Return the root widget

    def showUsernamePopup(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.username_input = TextInput(hint_text='Enter your name', multiline=False)
        submit_button = Button(text='Submit', size_hint_y=None, height=40)
        submit_button.bind(on_press=self.onSubmitUsername)
        content.add_widget(self.username_input)
        content.add_widget(submit_button)
        self.popup = Popup(title='Username', content=content, size_hint=(0.75, 0.5))
        self.popup.open()

    def onSubmitUsername(self, instance):
        self.username = self.username_input.text.strip()
        if self.username:
            self.popup.dismiss()
            self.buildChatInterface()
        else:
            # Optionally, display an error message or keep the popup open
            pass

    def buildChatInterface(self):
        # Clear existing widgets from the root
        self.root.clear_widgets()

        # Main layout for chat interface
        chat_layout = BoxLayout(orientation='vertical')

        # Display area for chat messages
        self.chat_history = Label(size_hint_y=None, valign='top', markup=True)
        self.chat_history.bind(texture_size=self.chat_history.setter('size'))

        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.scroll_view.add_widget(self.chat_history)

        # Text input for message typing
        self.message_input = TextInput(size_hint=(1, 0.1), multiline=False)

        # Send button
        self.send_button = Button(text='Send', size_hint=(1, 0.1))
        self.send_button.bind(on_press=self.sendMessage)

        # Add widgets to the chat layout
        chat_layout.add_widget(self.scroll_view)
        chat_layout.add_widget(self.message_input)
        chat_layout.add_widget(self.send_button)

        # Add the chat layout to the root widget
        self.root.add_widget(chat_layout)

        # Initialize client backend
        self.client_backend = ClientBackend(IP, 3232, gui_mode=True, gui_app=self, username=self.username)

        # Start receiving messages
        Thread(target=self.client_backend.recieveMessage, daemon=True).start()

    def sendMessage(self, instance):
        message = self.message_input.text.strip()
        if message:
            self.client_backend.sendMessage(message)
            self.message_input.text = ''

    def updateChatHistory(self, message):
        # Update chat history safely on the main thread
        self.chat_history.text += message + '\n'
        self.scroll_view.scroll_y = 0  # Scroll to the bottom


if __name__ == '__main__':
    ChatClientApp().run()
