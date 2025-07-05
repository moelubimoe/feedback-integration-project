import pika
import json

def publish_to_queue(data: dict, queue_name: str = "feedback"):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    body = json.dumps(data)
    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=body,
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()
