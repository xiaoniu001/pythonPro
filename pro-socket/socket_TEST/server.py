# coding: utf-8

import socket

s = socket.socket()

host = socket.gethostname()
print(host)

s.bind((host, 1234))

s.listen(5)

while True:
    c, address = s.accept()
    print(c)
    print("Got connect from {}".format(address))
    print(c.recv(1024))
    c.sendall(b"Thank you for connecting")
    # c.close()
