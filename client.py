import asyncore
import socket

HOST = "localhost"
PORT = 12345

class EchoClient(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((HOST, PORT))
        self.buffer = b"HELLO WORLD"

    def handle_connect(self):
        print("connect")

    def writeable(self):
        return (len(self.buffer) > 0)

    def handle_read(self):
        data = self.recv(1024)
        if data:
            print("READ", data)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

    def handle_close(self):
        print("close")
        self.close()

server = EchoClient(HOST, PORT)
asyncore.loop()

