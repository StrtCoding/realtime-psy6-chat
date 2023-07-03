import os

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, QThread, Slot
import socketio


from views.chat import ChatForm
from controllers.login import LoginWindow


class MessageListener(QThread):
    message = Signal(str)
    sio = socketio.Client()

    def run(self):
        self.sio.on('message', self.receive_msg)
        server_url = os.environ['SERVER_URL']
        self.sio.connect(server_url)
        self.message.emit("Connection to chat server completed")
    
    def receive_msg(self, msg):
        self.message.emit(msg)
    
    def send_msg(self, msg):
        self.sio.emit("message", msg)
    
    def server_logout(self):
        self.sio.disconnect()

class ChatWindow(QWidget, ChatForm):

    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setupUi(self)

        self.sendButton.clicked.connect(self.send_messages)
        self.logoutButton.clicked.connect(self.logout)

        self.message_listener = MessageListener()
        self.message_listener.message.connect(self.receive_message)

        self.message_listener.start()

    @Slot(str)
    def receive_message(self, message):
        self.chatTextEdit.append(message)
        self.chatTextEdit.setAlignment(Qt.AlignLeft)
    
    def send_messages(self):
        message = self.messageLineEdit.text().strip()

        message = f"{self.username}: {message}"
        self.message_listener.send_msg(message)
        self.messageLineEdit.clear()
    
    def logout(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
        self.message_listener.server_logout()
