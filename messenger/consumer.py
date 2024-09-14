#!/usr/bin/env python3
import pika, os
from src.data_collector import populate_db
url = os.environ.get('CLOUDAMQP_URL', 'amqps://zgumrvzp:llQpp-5zgHhcE2yTSodx78wT0onMsakK@whale.rmq.cloudamqp.com/zgumrvzp')
params = pika.URLParameters(url)

def consume_message():
    """
    Function that calls a database population function in the collector if it collects a message
    :rtype: object
    """
    connection = pika.BlockingConnection(params)
    channel = connection.channel() # start a channel
    channel.queue_declare(queue='hello') # Declare a queue
    def callback(ch, method, properties, body):
        print(" [x] Received " + body.decode("utf-8"))
        populate_db()
    channel.basic_consume('hello',
                          callback,
                          auto_ack=True)

    print(' [*] Waiting for messages:')
    channel.start_consuming()
    connection.close()