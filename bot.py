import requests
import os
import time
import json

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
MAX_TOKEN = os.environ.get("MAX_TOKEN")

def send_telegram(text):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Ошибка: нет токена или Chat ID")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=30)
        if r.status_code == 200:
            print(f"✅ Отправлено: {text[:50]}...")
        else:
            print(f"❌ Ошибка: {r.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def get_max_messages():
    """Проверяет подключение к Макс через API"""
    try:
        # Используем правильный адрес API Макс
        url = "https://api.max.ru/v1/messages"
        headers = {
            "Authorization": f"Bearer {MAX_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        r = requests.get(url, headers=headers, timeout=10)
        
        if r.status_code == 200:
            return r.json()
        else:
            send_telegram(f"⚠️ Ошибка API Макс: {r.status_code}")
            return None
    except Exception as e:
        send_telegram(f"⚠️ Ошибка подключения: {e}")
        return None

if __name__ == "__main__":
    print("🤖 Бот запущен")
    send_telegram("✅ Бот запущен и работает!")
    
    # Проверка токена Макс
    if not MAX_TOKEN:
        send_telegram("❌ Токен Макс не добавлен в переменные окружения")
    else:
        send_telegram("✅ Токен Макс найден")
        
        # Пробуем подключиться к API
        result = get_max_messages()
        if result is not None:
            send_telegram("✅ Подключение к Макс успешно!")
            send_telegram(f"📊 Получено сообщений: {len(result)}")
        else:
            send_telegram("⚠️ Не удалось подключиться к Макс. Возможно, токен устарел или неправильный эндпоинт.")
    
    while True:
        time.sleep(60)
