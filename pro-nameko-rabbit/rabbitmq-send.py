#coding: utf-8

import pika
import sys

# establish a connection with RabbitMQ server

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))

# create a hello queue
# Rabbitmq doesn't allow you to redefine an existing queue with different parameters

channel = connection.channel()
channel.queue_declare(queue="Hello", durable=True)

# sent directly to the queue through an exchange
message = ''.join(sys.argv[1:])
channel.basic_publish(exchange="", routing_key="Hello", body=message)

print(" [x] Sent %r" % message)

connection.close()