import requests
import os
import time
import json
import websocket

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
    """Обрабатывает входящие сообщения из WebSocket"""
    try:
        data = json.loads(message)
        print(f"📩 Получено: {data}")
        
        # Проверяем, есть ли в данных сообщение
        if "message" in data:
            msg = data["message"]
            if msg.get("text"):
                sender = msg.get("from", {}).get("name", "Неизвестный")
                text = msg.get("text", "")
                send_telegram(f"📩 {sender}: {text}")
        
        # Альтернативный формат сообщений
        elif "text" in data and "from" in data:
            sender = data.get("from", {}).get("name", "Неизвестный")
            text = data.get("text", "")
            send_telegram(f"📩 {sender}: {text}")
            
    except Exception as e:
        print(f"⚠️ Ошибка обработки: {e}")

def on_error(ws, error):
    print(f"⚠️ WebSocket ошибка: {error}")
    send_telegram(f"⚠️ Ошибка WebSocket: {error}")

def on_close(ws, close_status_code, close_msg):
    print("🔌 WebSocket закрыт")
    send_telegram("🔌 Соединение с Макс разорвано")

def on_open(ws):
    print("✅ WebSocket подключен")
    send_telegram("✅ Подключение к Макс установлено. Ожидаю сообщения...")

def connect_websocket():
    """Подключается к WebSocket Макс"""
    try:
        # Формируем URL для WebSocket
        ws_url = f"wss://web.max.ru/ws"
        headers = {
            "Authorization": f"Bearer {MAX_TOKEN}",
            "Origin": "https://web.max.ru"
        }
        
        ws = websocket.WebSocketApp(ws_url,
                                    header=headers,
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.run_forever()
    except Exception as e:
        send_telegram(f"❌ Ошибка подключения к WebSocket: {e}")
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    send_telegram("🚀 Бот запущен")
    
    if not MAX_TOKEN:
        send_telegram("❌ Токен Макс не найден")
    else:
        send_telegram("✅ Токен Макс найден")
        connect_websocket()
