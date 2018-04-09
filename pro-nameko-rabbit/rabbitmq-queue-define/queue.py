# coding: utf-8

import pika
import sys
import random

class Rabbitmq(object):
	"""define a Rabbitmq"""

	def __init__(self):
	
		self.connection=None
		self.channel=None
		

	def creat_channel(self, IP):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(IP))
		self.channel = self.connection.channel()
	

	def creat_queue(self, IP, Name):
		self.creat_channel(IP)
		queue = self.channel.queue_declare(queue=Name, durable=True)
		return queue


	def send_message(self, message, Name):
		self.channel.basic_publish(exchange="", routing_key=Name, body=message,
			properties=pika.BasicProperties(delivery_mode=2))# make message persistent
		print(" [x] Sent %r" % message)
		self.connection.close()


if __name__ == '__main__':
	rabbitmq = Rabbitmq()
	queue = rabbitmq.creat_queue("localhost", "task_queue")
	message = random.randint(1,10)
	print(message)
	rabbitmq.send_message(str(message), "task_queue")

		
		