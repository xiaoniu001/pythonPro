# coding: utf-8

import socket

from concurrent.futures import ThreadPoolExecutor
import time

pool = ThreadPoolExecutor(10000)


def tcp_client():
	s = socket.socket()
	s.connect(("127.0.0.1", 1234))
	while True:
		s.sendall(b"I'm client ,i will connect you")
		print(s.recv(1024))
		time.sleep(5)


for i in range(10000):
	pool.submit(tcp_client)
