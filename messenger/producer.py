#!/usr/bin/env python3
import pika, os

url = os.environ.get('CLOUDAMQP_URL')
params = pika.URLParameters(url)

def send_message(search_input):
    """
    Producer function that sends a message to the consumer which populates the database
    :rtype: object
    """
    connection = pika.BlockingConnection(params)
    channel = connection.channel() # start a channel
    channel.queue_declare(queue='hello') # Declare a queue
    channel.basic_publish(exchange='',
                            routing_key='hello',
                            body=search_input)
    print(" [x] Sent 'Hello World!'")
    connection.close()