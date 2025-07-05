import pika
import json

def callback(ch, method, properties, body):
    data = json.loads(body)
    print("✅ Новое обращение получено из очереди:")
    print(data)
    # Тут ты можешь логировать, сохранять в БД, отправлять email и т.д.
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker(queue_name: str = "feedback"):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print("👂 Воркер запущен. Ожидает сообщения...")
    channel.start_consuming()

if __name__ == "__main__":
    start_worker()
