import asyncore
import socket
import logging

# https://github.com/nicolargo/pythonarena/blob/master/asyncore/portscan.py

# TODO: find_peers function, which scans available port range and asks other peers which peers it knows about
# TODO: Better interface for working with overall p2p client.
#
#    import p2p
#
#    peer = p2p.connect("localhost", (55560, 55580))
#    peer.find_peers()
#    peers = peer.get_peers()
#    peer.message("Hello World")
#    peer.onMessage((msg) => { console.log(msg); })
#

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S') 

HOST = "localhost"
PORT_RANGE = range(55568, 55578)

class EchoClient(asyncore.dispatcher):
    def __init__(self, host, port_range):
        asyncore.dispatcher.__init__(self)
        self.host = host
        self.port_range = port_range
        self.buffer = b"HELLO WORLD"
        self.reconnect()

    def reconnect(self):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        for port in self.port_range:
            try:
                self.log("Attempting to connect to %s:%d" % (self.host, port))
                self.connect((self.host, port))
                self.port = port
                self.log("Looks like host is available")
                return
            except Exception as e:
                self.log("Error connecting to %s:%d" % (self.host, port))

    def handle_connect(self):
        self.log("Successfully connected to %s:%d" % (self.host, self.port))

    def writeable(self):
        return (len(self.buffer) > 0)

    def handle_read(self):
        data = self.recv(1024)
        if data:
            self.log("Received '%s' from SERVER" % (data,)) 

    def handle_write(self):
        if self.buffer:
            self.log("Sending '%s' to SERVER" % self.buffer)
            sent = self.send(self.buffer)
            self.buffer = self.buffer[sent:]

    def handle_close(self):
        self.log("Closed connection to %s:%d" % (self.host, self.port))
        self.close()
        self.host = None
        self.port = None

    def log(self, msg):
        logging.info("CLIENT: %s", msg)

class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(8192)
        if data:
            logging.info("SERVER: Received '%s' from CLIENT" % data)
            logging.info("SERVER: Sending '%s' to CLIENT" % data)
            self.send(data)

class EchoServer(asyncore.dispatcher):
    def __init__(self, host, port_range):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.set_reuse_addr()
        for port in port_range:
            if self.attempt_connect(port):
                break
        self.listen(5)

    def attempt_connect(self, port):
        try:
            self.bind((self.host, port))
            self.port = port
            self.log("Server found open port and launched on %s:%d" % (self.host, port))
            return True
        except OSError:
            self.log("Port %d is already being used" % (port,))
        except:
            print("Exception")

        return False

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            self.log("Incoming connection from %s" % repr(addr))
            handler = EchoHandler(sock)

    def log(self, msg):
        logging.info("SERVER: %s", msg)

server = EchoServer(HOST, PORT_RANGE)

client = EchoClient(HOST, PORT_RANGE)

asyncore.loop()

