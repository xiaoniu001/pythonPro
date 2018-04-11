# coding: utf-8

import pika
import sys
import random

class Rabbitmq(object):
	"""define a Rabbitmq"""

	def __init__(self):
	
		self.connection=None
		self.channel=None
		

	def creat_channel(self, IP, exchange):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(IP))
		self.channel = self.connection.channel()
		self.channel.exchange_declare(exchange=exchange, exchange_type="fanout")
	

	def creat_queue(self, IP, Name, exchange):
		self.creat_channel(IP, exchange)
		if Name:
			queue = self.channel.queue_declare(queue=Name, durable=True)
			return queue
		else:
			return False
		

	def send_message(self, message, Name, exchange):
		if Name:
			self.channel.basic_publish(exchange="", routing_key=Name, body=message,
				properties=pika.BasicProperties(delivery_mode=2))# make message persistent
		else:
			self.channel.basic_publish(exchange=exchange, routing_key='', body=message,
				properties=pika.BasicProperties(delivery_mode=2))# make message persistent
		print(" [x] Sent %r" % message)
		self.connection.close()


if __name__ == '__main__':
	rabbitmq = Rabbitmq()
	queue = rabbitmq.creat_queue("localhost", "", "logs")
	message = random.randint(1,10)
	print(message)
	rabbitmq.send_message(str(message), "", "logs")

		
		