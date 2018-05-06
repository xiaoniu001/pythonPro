# coding: utf-8

import socket

s = socket.socket()

# host = socket.gethostname()
# print(host)

s.connect(("192.168.72.1", 1234))
s.sendall(b"I'm client ,i will connect you")
print(s.recv(1024))
# s.close()
