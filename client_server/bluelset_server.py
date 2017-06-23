import bluelet

def echoer(conn):
    while True:
        data = yield conn.recv(1024)
        if not data:
            break
        print "CLIENT:", data
        yield conn.sendall(data)

bluelet.run(
    bluelet.server('127.0.0.1', 4915, echoer)
)
