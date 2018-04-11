# coding:utf-8

import pika
import time
from queue import Rabbitmq

class Worker(object):
	"""define worker"""

	def __init__(self, rabbitmq):
		self.rabbitmq = rabbitmq


	def callback(self, ch, method, properties, body):
		print("[x] Received %r" % body)
		time.sleep(int(body))
		print("[x] Done")
		ch.basic_ack(delivery_tag=method.delivery_tag)
		
	
	def consume(self, rabbitmq, Name):
		print(' [*] Waiting for messages. To exit press CTRL+C')
		self.rabbitmq.channel.queue_bind(exchange="logs", queue=Name)
		# This tells RabbitMQ not to give more than one message to a worker at a time
		self.rabbitmq.channel.basic_qos(prefetch_count=1)
		self.rabbitmq.channel.basic_consume(self.callback,
		 	queue=Name)
		self.rabbitmq.channel.start_consuming()


if __name__ == '__main__':
	rabbitmq = Rabbitmq()
	queue = rabbitmq.creat_queue("localhost","", "logs")
	if not queue:
		result = rabbitmq.channel.queue_declare(exclusive=True)
		queue_name = result.method.queue
	worker = Worker(rabbitmq)
	worker.consume(rabbitmq, queue_name)