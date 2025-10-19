# testing
import pika
import json
import os

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"Notification received: {message['message']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')
    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()
    queue = 'todo_notifications'
    channel.queue_declare(queue=queue, durable=False)
    channel.basic_consume(queue=queue, on_message_callback=callback)
    print('Notifier service waiting for messages...')
    channel.start_consuming()

if __name__ == '__main__':
    main()