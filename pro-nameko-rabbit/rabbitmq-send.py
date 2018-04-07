#coding: utf-8

import pika
import sys

# establish a connection with RabbitMQ server

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))

# create a hello queue

channel = connection.channel()
channel.queue_declare(queue="Hello")

# sent directly to the queue through an exchange
message = ''.join(sys.argv[1:])
channel.basic_publish(exchange="", routing_key="Hello", body=message)

print(" [x] Sent %r" % message)

connection.close()