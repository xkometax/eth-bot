import time
import requests
from telegram import Bot

BOT_TOKEN = "8003693652:AAFFfO6_-X3Sy_UuHRWeOIE__oSZN-xZWF8"
CHAT_ID = "517477141"
CHECK_INTERVAL = 300  # 5 минут
STEP = 10  # шаг в долларах

bot = Bot(token=BOT_TOKEN)

def get_eth_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
        response = requests.get(url)
        return response.json()["ethereum"]["usd"]
    except Exception as e:
        print("Ошибка получения цены:", e)
        return None

last_notified_price = None

print("✅ Бот запущен. Ожидаем движение ETH...")

while True:
    price = get_eth_price()
    if price:
        rounded = round(price / STEP) * STEP
        if rounded != last_notified_price:
            direction = "🔼 ETH вырос" if last_notified_price and rounded > last_notified_price else "🔽 ETH упал"
            message = f"{direction} до ${rounded}"
            try:
                bot.send_message(chat_id=CHAT_ID, text=message)
                print("[📨 Отправлено]:", message)
                last_notified_price = rounded
            except Exception as e:
                print("Ошибка отправки:", e)
        else:
            print(f"[ℹ️] ETH стабильна: ${price}")
    else:
        print("[⚠️] Не удалось получить цену.")

    time.sleep(CHECK_INTERVAL)
