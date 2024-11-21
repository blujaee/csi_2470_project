# File path: server_dashboard.py

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

# Define the GUI layout for the dashboard
class ServerClientGUI(BoxLayout):
    def __init__(self, **kwargs):
        super(ServerClientGUI, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Server status section
        self.server_status_label = Label(text="Server Status: [OFFLINE]", font_size=18)
        self.add_widget(self.server_status_label)

        self.server_control_btn = Button(text="Start Server", size_hint=(1, 0.2))
        self.server_control_btn.bind(on_press=self.toggle_server_status)
        self.add_widget(self.server_control_btn)

        # Chat stats section
        chat_stats_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        chat_stats_layout.add_widget(Label(text="Total Chats: "))
        self.total_chats_label = Label(text="0")
        chat_stats_layout.add_widget(self.total_chats_label)
        self.add_widget(chat_stats_layout)

        # User management section
        user_mgmt_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        user_mgmt_layout.add_widget(Label(text="New User: "))
        self.new_user_input = TextInput(hint_text="Enter username", multiline=False)
        user_mgmt_layout.add_widget(self.new_user_input)
        self.add_widget(user_mgmt_layout)

        self.add_user_btn = Button(text="Add User", size_hint=(1, 0.2))
        self.add_user_btn.bind(on_press=self.add_user)
        self.add_widget(self.add_user_btn)

        # Logs display section
        self.logs_label = Label(text="Logs:\n", size_hint=(1, 0.4), halign='left', valign='top', text_size=(self.width, None))
        self.add_widget(self.logs_label)

        self.refresh_logs_btn = Button(text="Refresh Logs", size_hint=(1, 0.2))
        self.refresh_logs_btn.bind(on_press=self.refresh_logs)
        self.add_widget(self.refresh_logs_btn)

    # Toggle server status
    def toggle_server_status(self, instance):
        if "Start" in self.server_control_btn.text:
            self.server_status_label.text = "Server Status: [ONLINE]"
            self.server_control_btn.text = "Stop Server"
        else:
            self.server_status_label.text = "Server Status: [OFFLINE]"
            self.server_control_btn.text = "Start Server"

    # Add a user (for example purposes, append username to logs)
    def add_user(self, instance):
        username = self.new_user_input.text.strip()
        if username:
            self.logs_label.text += f"Added user: {username}\n"
            self.new_user_input.text = ""

    # Refresh logs (example placeholder functionality)
    def refresh_logs(self, instance):
        self.logs_label.text += "Logs refreshed...\n"


# App class
class ServerDashboardApp(App):
    def build(self):
        return ServerClientGUI()


# Main entry point
if __name__ == "__main__":
    ServerDashboardApp().run()
