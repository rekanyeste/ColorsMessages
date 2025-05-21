import pika
import time
import random

connected = False
while not connected:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        connected = True
    except Exception as e:
        print(f"[Producer] Waiting for RabbitMQ... {e}")
        time.sleep(2)

channel = connection.channel()
channel.queue_declare(queue='colorQueue')

colors = ['RED', 'GREEN', 'BLUE']

print("[Producer] Started sending messages.")

while True:
    color = random.choice(colors)
    channel.basic_publish(exchange='', routing_key='colorQueue', body=color)
    time.sleep(0.5)
