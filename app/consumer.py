import json
import pika
import time
import os
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from webhook import send_telegram_message  # ⚠️ без 'app.' — запускается напрямую

# ✅ Настройка подключения к PostgreSQL
POSTGRES_USER = os.getenv("POSTGRES_USER", "feedback_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret_password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "feedback_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# SQLAlchemy ORM
Base = declarative_base()

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    message = Column(Text)
    source = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())

# Создаём движок и сессию
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание таблицы, если нет
Base.metadata.create_all(bind=engine)

def save_to_db(data, retries=3):
    for attempt in range(retries):
        try:
            db = SessionLocal()
            feedback = Feedback(
                name=data["name"],
                email=data["email"],
                message=data["message"],
                source=data["source"]
            )
            db.add(feedback)
            db.commit()
            db.close()
            print("💾 Заявка сохранена в БД")
            return
        except Exception as e:
            print(f"⚠️ Ошибка при записи в БД, попытка {attempt+1} из {retries}: {e}")
            time.sleep(1)
    print("❌ Не удалось записать в БД после нескольких попыток.")

def callback(ch, method, properties, body):
    print("📥 Получено сообщение из очереди:")
    try:
        data = json.loads(body)
        print(json.dumps(data, indent=2, ensure_ascii=False))

        save_to_db(data)

        # ✉️ Уведомление в Telegram
        send_telegram_message(data)

    except Exception as e:
        print("❌ Ошибка при обработке сообщения:", e)

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='feedback', durable=True)

    channel.basic_consume(queue='feedback', on_message_callback=callback, auto_ack=True)

    print("👂 Ожидание сообщений в очереди 'feedback'...")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
