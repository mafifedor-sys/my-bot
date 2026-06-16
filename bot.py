import asyncio
import os
import time
import requests
import max_api_python as Max  # Библиотека для работы с API Макс

# --- НАСТРОЙКИ ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
MAX_TOKEN = os.environ.get("MAX_TOKEN")  # <-- Этот новый секрет мы добавим позже
MAX_CHAT_ID = os.environ.get("MAX_CHAT_ID", "")  # <-- ID чата Макс, откуда будут пересылаться сообщения

# --- ФУНКЦИЯ ОТПРАВКИ В TELEGRAM ---
def send_telegram(text):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Ошибка: не настроены секреты Telegram")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=30)
        if r.status_code == 200:
            print(f"✅ Отправлено в Telegram: {text[:50]}...")
        else:
            print(f"❌ Ошибка Telegram: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"❌ Ошибка отправки в Telegram: {e}")

# --- ОСНОВНАЯ ЛОГИКА БОТА ---
async def main():
    print("🚀 Бот запускается и подключается к Макс...")

    if not MAX_TOKEN:
        send_telegram("❌ Ошибка: не найден токен Макс. Добавьте секрет MAX_TOKEN.")
        return

    # Инициализируем сессию Макс
    try:
        client = Max.Client(MAX_TOKEN)
        me = await client.get_me()
        print(f"✅ Подключен к Макс как: {me.name} (@{me.username})")
        send_telegram(f"✅ Бот подключен к Макс как: {me.name} (@{me.username})")
    except Exception as e:
        error_msg = f"❌ Ошибка подключения к Макс: {e}"
        print(error_msg)
        send_telegram(error_msg)
        return

    # Если указан ID чата, то подписываемся на входящие сообщения в этом чате
    if MAX_CHAT_ID:
        send_telegram(f"🔄 Бот слушает чат с ID: {MAX_CHAT_ID}")
        print(f"🔄 Слушаем чат: {MAX_CHAT_ID}")

        # Запускаем бесконечный цикл для получения обновлений
        while True:
            try:
                # Получаем последние сообщения из чата
                messages = await client.get_history(chat_id=int(MAX_CHAT_ID), count=1)
                if messages:
                    last_msg = messages[0]
                    # Простая логика: пересылаем только текстовые сообщения от других
                    if hasattr(last_msg, 'text') and last_msg.from_ != me.id:
                        sender = await client.get_user(last_msg.from_)
                        text = last_msg.text
                        send_telegram(f"📩 {sender.name}: {text}")
                await asyncio.sleep(5)  # Проверяем каждые 5 секунд
            except Exception as e:
                print(f"⚠️ Ошибка при получении сообщений: {e}")
                await asyncio.sleep(10)
    else:
        print("ℹ️ ID чата не указан. Бот запущен, но не слушает конкретный чат.")

if __name__ == "__main__":
    # Отправляем приветственное сообщение
    send_telegram("✅ Бот на Bothost запущен и готов к работе с Макс!")
    asyncio.run(main())
