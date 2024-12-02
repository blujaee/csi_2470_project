# Import necessary Kivy modules for creating the GUI
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup # used in username popup
from threading import Thread # used for concurrent processes

from ClientsIP import IP
from ClientBackend import ClientBackend 

# Define the ChatClientApp class, with argument App
class ChatClientApp(App):
    # The build method sets up the GUI layout and initializes the app
    # Using self as a parameter allows modifying this instance of the class
    def build(self):
        self.title = "Chat Client"  # Set the title of the application window

        # Create the root widget as a BoxLayout
        # It is Kivy convention to use root for this variable, but it can be named anything
        self.root = BoxLayout()  # BoxLayout arranges child widgets in a linear fashion

        # Prompt the user for their username before proceeding to the chat
        self.username = ''  # Initialize an empty username
        self.showUsernamePopup()  # Call the showUsernamePopup method to display a popup for username input

        return self.root  # Return the root widget to be displayed
        # So when build function is run, the root widget (screen) will be displayed

    # Display a popup for the user to enter their username
    def showUsernamePopup(self):
        # Create a vertical layout for the popup's content
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)  # padding and spacing add space around and between widgets

        # Input field for the username
        self.username_input = TextInput(hint_text='Enter your name', multiline=False)  # hint_text gives placeholder text; multiline=False restricts to a single line

        # Button to submit the username
        # Creates a new instance of the Button class from Kivy
        # size_hint_y=None allows manual height control
        submit_button = Button(text='Submit', size_hint_y=None, height=40)
        # Bind the button's press event to the onSubmitUsername method 
        # So basically when the button is pressed, the onSubmitUsername method will be called.
        submit_button.bind(on_press=self.onSubmitUsername)  

        # Add the username input field and button to the popup content
        # add_widget() is a Kivy function to add a child widget to a parent widget
        content.add_widget(self.username_input)  # Add the input field to the layout
        content.add_widget(submit_button)  # Add the button below the input field

        # Create and display the popup with the layout as content
        # size_hint controls popup size as a percentage of the screen
        # Popup is a CLASS that we got from Kivy 
        # self.Popup stores a new instance of Popup in the current instance so we can refer to it later
        self.popup = Popup(title='Username', content=content, size_hint=(0.75, 0.5))
        # Open the popup for user interaction
        # .open() is a METHOD that shows our popup that we just stored in the current instance (self)
        self.popup.open()  

    # Handle the username submission
    def onSubmitUsername(self, instance):
        # .strip() is a METHOD that removes extra spaces from an input. 
        self.username = self.username_input.text.strip()
        if self.username:  # AKA: "If a valid username is entered"
            self.popup.dismiss()  # Close the popup
            self.buildChatInterface()  # Build/launch the main chat interface
        else:
            # shuts down the server from the backend if username isn't entered
            # we use the shutdown method from serverBackend bc it is more 
            # clean than just automatically stopping the server
            self.server_backend.shutdown()

    # Build the main chat interface
    # buildChatInterface is a METHOD within the ChatClientApp class
    def buildChatInterface(self):
        # Clear all existing widgets from the root, gets rid of username popup
        self.root.clear_widgets()  

        # Create a vertical layout for the chat interface
        chat_layout = BoxLayout(orientation='vertical')

        # create an instance of the Label CLASS for displaying chat messages
        # valign='top' aligns text at the top; markup=True allows rich text formatting
        self.chat_history = Label(size_hint_y=None, valign='top', markup=True) 
        # use .bind() METHOD to allow size of the Label instance to change 
        self.chat_history.bind(texture_size=self.chat_history.setter('size'))

        # Create an instance of ScrollView CLASS to make the chat history scrollable
        # size_hint controls how much space the widget occupies
        self.scroll_view = ScrollView(size_hint=(1, 0.8))
         # Add the chat history label that we created above inside the ScrollView
        self.scroll_view.add_widget(self.chat_history) 

        # Input field for typing messages
        # Creates an instance of the TextInput CLASS
        # multiline=False ensures single-line input
        self.message_input = TextInput(size_hint=(1, 0.1), multiline=False)  

        # Button to send messages
        # Creates an instance of the Button CLASS
        # size_hint=(1, 0.1) sets the button to be full-width and 10% height
        self.send_button = Button(text='Send', size_hint=(1, 0.1))  
        # use .bind() METHOD so when the button is pressed, the sendMessage method is triggered
        self.send_button.bind(on_press=self.sendMessage) 

        # Add chat interface widgets to the layout
        # uses add_widget() METHOD to add child widgets to parent widget
        # Add the ScrollView for message display
        chat_layout.add_widget(self.scroll_view)  
        # Add the message input field
        chat_layout.add_widget(self.message_input)  
        # Add the send button
        chat_layout.add_widget(self.send_button)  

        # Add the chat layout to the root widget
        self.root.add_widget(chat_layout)

        # Initialize the client backend with required parameters
        # Calls ClientBackend class to handle network communication; 
        # IP is the server address stored in ClientsIP.py, 3232 is the port
        # gui_mode determines whether the app will run in gui or terminal
        # gui_app passes the current instance of the ChatClientApp CLASS to ClientBackend CLASS
        # Passes the username entered by the user to ClientBackend CLASS
        self.client_backend = ClientBackend(
            IP, 3232, gui_mode=True, gui_app=self, username=self.username
        )  

        # Start receiving messages in a separate thread
        # This prevents blocking the event loop of the app
        # Thread() is a CLASS
        # .start() is a method that triggers the start of the instance of Thread() CLASS
        # daemon=True ensures the thread stops when the app exits
        Thread(target=self.client_backend.recieveMessage, daemon=True).start()  

    # Handle sending messages
    def sendMessage(self, instance):
        # new VARIABLE message is just the user input with spaces removed
        message = self.message_input.text.strip() 
        # if the message is not empty
        if message:
            # Use the sendMessage METHOD in ClientBackend CLASS to send the message
            self.client_backend.sendMessage(message)
            # Clear the input field after sending
            self.message_input.text = ''  

    # Update the chat history with the new message
    def updateChatHistory(self, message):
        # Appends the new message to the chat history
        self.chat_history.text += message + '\n' 
        # Scroll to the bottom to show the latest message
        # .scroll_y is a PROPERTY of ScrollView widget in Kivy
        self.scroll_view.scroll_y = 0 

# Entry point for the application
# Prevents application from automatically running if it was to be imported
if __name__ == '__main__':
    # Create an instance of the ChatClientApp CLASS and run it
    ChatClientApp().run()  # Run the application
