#!/usr/bin/env python3
import pika, os
from src.data_collector import set_input

url = os.environ.get('CLOUDAMQP_URL', 'amqps://zgumrvzp:llQpp-5zgHhcE2yTSodx78wT0onMsakK@whale.rmq.cloudamqp.com/zgumrvzp')
params = pika.URLParameters(url)
params.socket_timeout = 5

def callback(ch, method, properties, body):
    set_input(str(body))

def consume_message():
    """
    Consumes message received through CloudAMQP
    :rtype: object
    """
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='input')
    channel.basic_consume('input',
                            callback,
                            auto_ack=True)
    channel.start_consuming()
    connection.close()

if __name__ == "__main__":
    consume_message()