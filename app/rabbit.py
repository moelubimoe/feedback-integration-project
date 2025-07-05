import pika
import json

def publish_feedback(data: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="feedback")

    message = json.dumps(data)
    channel.basic_publish(exchange="", routing_key="feedback", body=message)

    connection.close()
