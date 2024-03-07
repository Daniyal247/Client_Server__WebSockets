import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton

class ClientApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.start_client()

    def initUI(self):
        self.setWindowTitle('Client')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.input_line = QLineEdit()
        layout.addWidget(self.input_line)

        send_button = QPushButton('Send')
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)

        self.setLayout(layout)

    def start_client(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 9999))
        print("Connected to the server.")

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def receive_messages(self):
        while True:
            try:
                response = self.client_socket.recv(1024).decode('utf-8')
                if response:
                    self.text_edit.append("Server: " + response)
            except Exception as e:
                print(f"Error receiving message from server: {str(e)}")
                break

    def send_message(self):
        message = self.input_line.text()
        if message:
            self.text_edit.append("You: " + message)  # Append sent message to text edit
            self.client_socket.send(message.encode('utf-8'))
            self.input_line.clear()
        else:
            print("Please enter a message.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client_app = ClientApp()
    client_app.show()
    sys.exit(app.exec_())
