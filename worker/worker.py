import pika
import time
import random
import os

client_id = os.getenv('CLIENT_ID', 'unknown')

connected = False
while not connected:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        connected = True
    except Exception:
        time.sleep(2)

channel = connection.channel()
channel.queue_declare(queue='colorQueue')

def callback(ch, method, properties, body):
    processing_time = random.randint(2000, 9000) / 1000
    time.sleep(processing_time)

    try:
        processed_connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        processed_channel = processed_connection.channel()
        processed_channel.queue_declare(queue='processedColors')

        message = f"Client {client_id}, processed a '{body.decode()}' message"
        processed_channel.basic_publish(
            exchange='',
            routing_key='processedColors',
            body=message
        )

        processed_connection.close()
    except Exception:
        pass

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='colorQueue', on_message_callback=callback)
channel.start_consuming()
