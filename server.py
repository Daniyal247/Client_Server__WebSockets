import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton

class ServerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.start_server()

    def initUI(self):
        self.setWindowTitle('Server')
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        # Text display area
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(False)
        layout.addWidget(self.text_edit)

        # Input area
        self.input_line = QLineEdit()
        layout.addWidget(self.input_line)

        # Send button
        send_button = QPushButton('Send')
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)

        self.setLayout(layout)

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 9999))
        self.server_socket.listen(5)
        print("Server listening on port 9999...")

        self.clients = []

        self.server_message_thread = threading.Thread(target=self.get_server_message)
        self.server_message_thread.start()

    def handle_client(self, client_socket, client_address):
        print(f"Accepted connection from {client_address}")
        self.text_edit.append(f"Accepted connection from {client_address}")

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            self.text_edit.append(f"Received from {client_address}: {data.decode('utf-8')}")

        print(f"Connection from {client_address} closed.")
        self.text_edit.append(f"Connection from {client_address} closed.")
        client_socket.close()

    def broadcast(self, message):
        for client in self.clients:
            try:
                client.send(message.encode('utf-8'))
            except:
                self.clients.remove(client)

    def get_server_message(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_handler.start()

    def send_message(self):
        message = self.input_line.text()
        self.text_edit.append("You: " + message)
        self.broadcast(message)
        self.input_line.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    server_app = ServerApp()
    server_app.show()
    sys.exit(app.exec_())
