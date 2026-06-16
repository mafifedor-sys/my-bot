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
    try:
        headers = {"Authorization": f"Bearer {MAX_TOKEN}"}
        url = "https://web.max.ru/api/v1/messages"  # Правильный эндпоинт
        r = requests.get(url, headers=headers, timeout=10)
        return r.json() if r.status_code == 200 else None
    except:
        return None

if __name__ == "__main__":
    print("🤖 Бот запущен")
    send_telegram("✅ Бот запущен и работает!")
    
    # Проверка токена Макс
    if MAX_TOKEN:
        send_telegram("✅ Токен Макс найден")
        # Проверяем подключение
        msgs = get_max_messages()
        if msgs:
            send_telegram("✅ Подключение к Макс успешно")
        else:
            send_telegram("⚠️ Не удалось подключиться к Макс. Проверьте токен.")
    else:
        send_telegram("❌ Токен Макс не добавлен в переменные окружения")
    
    # Бесконечный цикл
    while True:
        time.sleep(60)
