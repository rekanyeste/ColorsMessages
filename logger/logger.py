import pika
import time
import os

time.sleep(5)

rabbit_host = os.getenv('RABBIT_HOST', 'rabbitmq')
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters(host=rabbit_host, credentials=credentials)

connected = False
while not connected:
    try:
        connection = pika.BlockingConnection(parameters)
        connected = True
    except Exception as e:
        print(f"Waiting for RabbitMQ... {e}")
        time.sleep(2)

channel = connection.channel()
channel.queue_declare(queue='processedColors')

def callback(ch, method, properties, body):
    print(body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='processedColors', on_message_callback=callback)
channel.start_consuming()
