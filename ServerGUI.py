# Server GUI for the chat application using Kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from threading import Thread

from ServersIP import IP
from ServerBackend import ServerBackend


class ChatServerApp(App):
    def build(self):
        self.title = "Chat Server"

        # Main layout
        self.root = BoxLayout(orientation='vertical')

        # Scrollable text area for server logs
        self.log_history = Label(size_hint_y=None, valign='top')
        self.log_history.bind(texture_size=self.log_history.setter('size'))

        self.scroll_view_logs = ScrollView(size_hint=(1, 0.6))
        self.scroll_view_logs.add_widget(self.log_history)

        # Label to display connected users
        self.users_label = Label(text="Connected Users:", size_hint=(1, 0.4), halign='left', valign='top')
        self.users_label.bind(size=self.users_label.setter('texture_size'))

        self.scroll_view_users = ScrollView(size_hint=(1, 0.4))
        self.scroll_view_users.add_widget(self.users_label)

        # Add widgets to the layout
        self.root.add_widget(self.scroll_view_logs)
        self.root.add_widget(self.scroll_view_users)

        # Initialize server backend
        self.server_backend = ServerBackend(IP, 3232, gui_mode=True, gui_app=self)

        # Start server listening in a separate thread
        Thread(target=self.server_backend.listen, daemon=True).start()

        return self.root

    def updateUserList(self, user_list):
        users_text = "Connected Users:\n" + "\n".join(user_list)
        self.users_label.text = users_text

    def updateServerLog(self, message):
        # Update server log safely on the main thread
        self.log_history.text += message + '\n'
        self.scroll_view_logs.scroll_y = 0  # Scroll to the bottom


if __name__ == '__main__':
    ChatServerApp().run()
