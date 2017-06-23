import asyncore
import socket

HOST = "localhost"
PORT_RANGE = range(5568, 5578)

'''
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
'''

class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(8192)
        if data:
            print("GOT", data)
            self.send(data)

class EchoServer(asyncore.dispatcher):
    def __init__(self, host, port_range):
        asyncore.dispatcher.__init__(self)
        self.port_range = port_range
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()

        for port in port_range:
            try:
                self.bind((host, port))
                print("Found open port on %d" % port)
                return
            except OSError:
                print("Port %d is already in use" % port)

        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print('Incoming connection from %s' % repr(addr))
            handler = EchoHandler(sock)

server = EchoServer(HOST, PORT_RANGE)
asyncore.loop()

