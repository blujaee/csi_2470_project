import kivy

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

    #return
    
def loadClientElements():
    return
