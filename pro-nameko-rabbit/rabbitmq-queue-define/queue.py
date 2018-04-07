# coding: utf-8

import pika

class Queue(object):
	"""define a queue"""
	
	connection = None


	def __init__(self, IP, Name):
		self.IP = IP
		self.Name = Name
		

	def creat_connection(self):
		connection = pika.BlockingConnection(pika.ConnectionParameters(self.IP))
		channel = connection.channel()
		return channel


	def creat_queue(self):
		channel = self.creat_connection()
		queue = channel.queue_declare(queue=self.Name, durable=True)
		return queue


	def send_message(self, message):
		queue = self.creat_queue()
		channel.basic_publish(exchange="", routing_key=queue, body=message)
		print(" [x] Sent %r" % message)
		self.creat_queue().connection.close()

		

		
		