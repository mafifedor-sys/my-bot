import requests
import os
import time

# Бот берет токены из секретных настроек на сайте Bothost
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(text):
    """Отправляет сообщение в ваш Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=30)
        print(f"✅ Отправлено: {text}")
        return r.json()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

if __name__ == "__main__":
    print("🤖 Бот запущен!")
    # Отправляем тест, чтобы убедиться, что всё работает
    send_telegram("✅ Бот на Bothost запущен и работает!")
    
    # Бесконечный цикл, чтобы бот не завершился
    while True:
        time.sleep(60)