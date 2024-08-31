#!/usr/bin/env python3
import json, pika

'''
Establish a connection to a RabbitMQ server.
localhost means we are connecting to the local
machine. However we can provide a IP address to
a different machine.
'''
conn = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = conn.channel()

'''
We create a queue just for transactions
'''
channel.queue_declare(queue="transactions")

channel.basic_publish(exchange="", routing_key="transactions",
                      body=json.dumps({
                          "card_num": 12340000,
                          "total": 4.10
                      }))