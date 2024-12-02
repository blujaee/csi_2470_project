# Server GUI for the chat application using Kivy

# Importing necessary libraries and modules
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from threading import Thread
import signal
import sys

from ServersIP import IP
from ServerBackend import ServerBackend

# Defines class ChatServerApp, which inherits from Kivy's App
class ChatServerApp(App):
    # build method sets up the GUI layout and initializes the server
    # Using self as a parameter lets us work with only our current instance of the class
    def build(self):
        self.title = "Chat Server"  # Sets the app window title

        # The main layout of the app, everything gets stacked vertically
        # root is Kivy convention for main widget
        self.root = BoxLayout(orientation='vertical')

        # A label to show server logs
        self.log_history = Label(size_hint_y=None, valign='top')  # Top-aligned text
        self.log_history.bind(texture_size=self.log_history.setter('size'))  # Auto-resize based on text size

        # Scroll view on the server logs (in case there are lots of them)
        # calls ScrollView class and sets size
        # calls add_widget method. this adds a label instance to ScrollView class
        self.scroll_view_logs = ScrollView(size_hint=(1, 0.6))  # Takes up 60% of the layout height
        self.scroll_view_logs.add_widget(self.log_history)  # Adds the log label to the scrollable area

        # A label to show the list of connected users
        # Creates the current instace of the Label class called users_label
        self.users_label = Label(text="Connected Users:", size_hint=(1, 0.4), halign='left', valign='top')  # Top-left aligned
        # binds the size of the Label class to the size of the widget so it auto-adjusts
        self.users_label.bind(texture_size=self.users_label.setter('size'))

        # Scroll view for the connected users
        # Creates the current insteance of the ScrollView class called scroll_view_users
        self.scroll_view_users = ScrollView(size_hint=(1, 0.4))  # Takes up 40% of the layout height
        # adds the previously created users_label instance to the scroll view area
        self.scroll_view_users.add_widget(self.users_label) 

        # Add both scroll views (logs and users) to the main layout
        self.root.add_widget(self.scroll_view_logs)
        self.root.add_widget(self.scroll_view_users)

        # creates a new instance of ServerBackend class on specific IP
        self.server_backend = ServerBackend(IP, 3232, gui_mode=True, gui_app=self)

        
        # Start the server in a separate thread. If i ran the server directly, 
        # it would block the event loop and freeze the GUI. Setting this as a daemon thread allows us 
        # to auto-exit the server once all other threads are done.
        # Thread() is a class provided in the python function module.
        # the arguments in class create an instance of ServerBackend class and excecute the listen methods 
        # in that class .start() is a method that starts the Thread() class 
        Thread(target=self.server_backend.listen, daemon=True).start()

        # Handle Ctrl+C
        # SIGINT is signal interrupt, triggered by ctrl+c
        signal.signal(signal.SIGINT, self.signal_handler)

        return self.root  # Return the main layout

    # Updates the user list in the GUI
    def updateUserList(self, user_list):
        # Format the connected user list as a single string
        users_text = "Connected Users:\n" + "\n".join(user_list)
        self.users_label.text = users_text  # Update the users label with the new list

    # Updates the server log in the GUI
    def updateServerLog(self, message):
        # Add the new log message to the log label
        self.log_history.text += message + '\n'
        self.scroll_view_logs.scroll_y = 0  # Scroll to the bottom to show the latest message

    # Handles when the app is closed using Ctrl+C or stop
    # so when ctrl+c is pressed, signal_handler method is called
    # important bc cleans up server. without this, program will be
    # immedietly terminated, and threads may still be running etc.
    def signal_handler(self, sig, frame):
        print("\nShutting down server via GUI...")  # Just a little goodbye message in the terminal
        self.server_backend.shutdown()  # Tell the server to clean up and stop
        sys.exit(0)  # Exit the app entirely

    # Handles when the GUI is closed manually (like clicking the close button)
    def on_stop(self):
        # Save chat records and shut down the server gracefully
        # Calls the shutdown method in this instance of ServerBackend
        self.server_backend.shutdown()

# Main entry point for the app
# This just means that ChatServerApp runs ONLY IF excecuted directly
# Prevents app from auto-starting when imported.
if __name__ == '__main__':
    # Create an instance of ChatServerApp class
    # .run() is a method in App class from Kivy that initializes the application, calls build() method
    # and starts app event loop
    ChatServerApp().run()