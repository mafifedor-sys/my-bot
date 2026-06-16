import asyncio
import os
import time
import requests
from max_api_python import Client

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
MAX_TOKEN = os.environ.get("MAX_TOKEN")

def send_telegram(text):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=30)
        print(f"✅ Отправлено: {text[:50]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

async def main():
    send_telegram("🚀 Бот запускается...")
    
    if not MAX_TOKEN:
        send_telegram("❌ Токен Макс не найден")
        return
    
    try:
        client = Client(MAX_TOKEN)
        me = await client.get_me()
        send_telegram(f"✅ Подключено к Макс как: {me.name}")
    except Exception as e:
        send_telegram(f"❌ Ошибка: {e}")
        return
    
    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
