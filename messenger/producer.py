#!/usr/bin/env python3
import pika, os
from messenger.consumer import consume_message

url = os.environ.get('CLOUDAMQP_URL', 'amqps://zgumrvzp:llQpp-5zgHhcE2yTSodx78wT0onMsakK@whale.rmq.cloudamqp.com/zgumrvzp')
params = pika.URLParameters(url)
params.socket_timeout = 5

def produce_message(search_input):
    """
    Produces message using CloudAMQP
    :rtype: object
    """
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='input')
    channel.basic_publish(exchange='',
                            routing_key='input',
                            body=search_input)
    connection.close()