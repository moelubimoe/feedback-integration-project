import httpx

TELEGRAM_BOT_TOKEN = "7889473471:AAHTJGGdg5Pugbv8sfs0anAGeGEMGUDPRFo"
TELEGRAM_CHAT_ID = "449074995"

def send_telegram_message(data: dict):
    text = (
        "📥 Новая заявка!\n\n"
        f"👤 Имя: {data['name']}\n"
        f"✉️ Email: {data['email']}\n"
        f"💬 Сообщение: {data['message']}\n"
        f"🌐 Источник: {data['source']}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        response = httpx.post(url, data=payload)
        response.raise_for_status()
        print("✅ Уведомление отправлено в Telegram")
    except httpx.HTTPError as e:
        print(f"❌ Ошибка при отправке в Telegram: {e}")
