import bluelet

def connecho():
    c = yield bluelet.connect("127.0.0.1", 4915)
    while True:
        yield c.sendall("HELLO WORLD")
        data = yield c.recv(1024)
        print("SERVER:", data)
        raw_input("HEY")

def main():
    yield bluelet.spawn(connecho())

bluelet.run(main())


