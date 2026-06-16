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
            print(f"❌ Ошибка Telegram: {r.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def get_max_chats():
    """Получает список чатов через веб-версию Макс"""
    try:
        url = "https://web.max.ru/api/v1/chats"
        headers = {
            "Authorization": f"Bearer {MAX_TOKEN}",
            "Content-Type": "application/json"
        }
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json()
        else:
            send_telegram(f"⚠️ Ошибка получения чатов: {r.status_code}")
            return None
    except Exception as e:
        send_telegram(f"⚠️ Ошибка: {e}")
        return None

def check_new_messages():
    """Проверяет новые сообщения (упрощённо)"""
    try:
        url = "https://web.max.ru/api/v1/messages"
        headers = {
            "Authorization": f"Bearer {MAX_TOKEN}",
            "Content-Type": "application/json"
        }
        params = {"limit": 10}  # Последние 10 сообщений
        r = requests.get(url, headers=headers, params=params, timeout=10)
        if r.status_code == 200:
            return r.json()
        else:
            return None
    except:
        return None

if __name__ == "__main__":
    print("🤖 Бот запущен")
    send_telegram("✅ Бот запущен и работает!")
    
    if not MAX_TOKEN:
        send_telegram("❌ Токен Макс не найден")
    else:
        send_telegram("✅ Токен Макс найден")
        
        # Проверяем доступ к чатам
        chats = get_max_chats()
        if chats:
            send_telegram(f"✅ Получено чатов: {len(chats)}")
        else:
            send_telegram("⚠️ Не удалось получить список чатов")
    
    # Основной цикл
    last_checked = time.time()
    while True:
        try:
            # Проверяем новые сообщения каждые 10 секунд
            if time.time() - last_checked > 10:
                messages = check_new_messages()
                if messages:
                    # Обработка сообщений (упрощённо)
                    for msg in messages:
                        if msg.get("text"):
                            sender = msg.get("from", {}).get("name", "Неизвестный")
                            text = msg.get("text", "")
                            send_telegram(f"📩 {sender}: {text}")
                last_checked = time.time()
        except Exception as e:
            print(f"⚠️ Ошибка в цикле: {e}")
        
        time.sleep(5)
