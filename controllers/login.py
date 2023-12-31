from PySide6.QtWidgets import QWidget
from views.login import LoginForm

class LoginWindow(QWidget, LoginForm):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.joinButton.clicked.connect(self.join_to_chat)

    def join_to_chat(self):
        username = self.usernameLineEdit.text()

        if username != '':
            from controllers.chat import ChatWindow
            self.chat_window = ChatWindow(username)
            self.chat_window.show()
            self.close()
        else:
            print("Username es obligatorio!")