# coding:utf-8

import pika
import time
# we're not yet sure which program to run first, so 
# it's a good practice to repeat declaring the queue in both programs
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="Hello")


def callback(ch, method, properties, body):
	print("[x] Received %r" % body)
	time.sleep(len(body))
	print("[x] Done")


channel.basic_consume(callback, queue="Hello", no_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()