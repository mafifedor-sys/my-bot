import asyncio
import requests
import os
from pymax import WebClient

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
MAX_TOKEN = os.environ.get("MAX_TOKEN")  # Ваш __oneme_auth токен

def send_telegram(text):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=30)
        print(f"✅ Отправлено в Telegram: {text[:50]}")
    except Exception as e:
        print(f"❌ Ошибка отправки в Telegram: {e}")

async def on_message(client, message):
    """Функция, которая будет вызываться при каждом новом сообщении."""
    # Фильтруем, чтобы не пересылать свои же сообщения
    if message.from_id == client.me.id:
        return
    # Отправляем уведомление в Telegram
    sender = await client.get_user(message.from_id)
    text = f"📩 **{sender.name}**: {message.text}"
    send_telegram(text)

async def main():
    print("🚀 Запуск UserBot...")
    if not MAX_TOKEN:
        send_telegram("❌ Ошибка: Токен MAX_TOKEN не найден.")
        return

    # Создаем WebClient для авторизации по токену от веб-версии
    client = WebClient(work_dir="cache", session_name="session.db")
    
    # Подписываемся на события
    client.on_message(on_message)  # Эта строчка "слушает" все новые сообщения [citation:10]

    # Запускаем клиента. Он сам авторизуется и поддерживает соединение.
    await client.start(token=MAX_TOKEN)  # Передаем токен сюда

    # Бесконечный цикл, чтобы бот не завершался
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    send_telegram("✅ Бот переходит в режим прослушки Макс...")
    asyncio.run(main())
