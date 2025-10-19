#!/usr/bin/env python3
"""Notifier service consuming messages from RabbitMQ."""

import json
import os

import pika


def callback(ch, method, properties, body):
    """Handle incoming messages from RabbitMQ."""
    message = json.loads(body)
    msg = message.get("message")
    print(f"Notification received: {msg}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    """Connect to RabbitMQ and start consuming messages."""
    rabbitmq_url = os.getenv(
        "RABBITMQ_URL", "amqp://guest:guest@localhost:5672/"
    )
    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()
    queue = "todo_notifications"
    channel.queue_declare(queue=queue, durable=False)
    channel.basic_consume(queue=queue, on_message_callback=callback)
    print("Notifier service waiting for messages...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
