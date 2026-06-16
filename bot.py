import requests
import os
import time
import json
import websocket
import threading

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
MAX_TOKEN = os.environ.get("MAX_TOKEN")

def send_telegram(text):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=30)
        if r.status_code == 200:
            print(f"✅ Отправлено: {text[:50]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def on_message(ws, message):
    try:
        data = json.loads(message)
        print(f"📩 Получено: {data}")
        
        # Проверяем разные форматы сообщений
        if "message" in data:
            msg = data["message"]
            if msg.get("text"):
                sender = msg.get("from", {}).get("name", "Неизвестный")
                text = msg.get("text", "")
                send_telegram(f"📩 {sender}: {text}")
        elif "text" in data and "from" in data:
            sender = data.get("from", {}).get("name", "Неизвестный")
            text = data.get("text", "")
            send_telegram(f"📩 {sender}: {text}")
        elif "body" in data:
            send_telegram(f"📩 {data}")
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")

def on_error(ws, error):
    print(f"⚠️ Ошибка: {error}")

def on_close(ws, close_status_code, close_msg):
    print("🔌 Отключено")
    # Переподключаемся через 5 секунд
    time.sleep(5)
    connect_websocket()

def on_open(ws):
    print("✅ Подключено")
    send_telegram("✅ Подключение к Макс установлено")

def connect_websocket():
    try:
        # Правильный формат WebSocket с токеном в URL
        ws_url = f"wss://web.max.ru/socket.io/?EIO=3&transport=websocket&token={MAX_TOKEN}"
        
        ws = websocket.WebSocketApp(ws_url,
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.run_forever()
    except Exception as e:
        send_telegram(f"❌ Ошибка: {e}")
        time.sleep(5)
        connect_websocket()

if __name__ == "__main__":
    send_telegram("🚀 Бот запущен")
    
    if not MAX_TOKEN:
        send_telegram("❌ Токен Макс не найден")
    else:
        send_telegram("✅ Токен Макс найден")
        connect_websocket()
