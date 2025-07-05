import sqlite3
import os

# Путь к БД
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "feedback.db")

data = {
    "name": "Тест Наташа",
    "email": "test@ya.ru",
    "message": "Проверка ручной записи",
    "source": "manual"
}

try:
    conn = sqlite3.connect(DB_PATH, timeout=10)
    c = conn.cursor()
    c.execute("""
        INSERT INTO feedback (name, email, message, source)
        VALUES (?, ?, ?, ?)
    """, (data["name"], data["email"], data["message"], data["source"]))
    conn.commit()
    print("✅ Запись вручную в БД прошла успешно.")
except Exception as e:
    print("❌ Ошибка при записи в БД:", e)
finally:
    conn.close()
