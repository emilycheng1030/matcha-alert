import requests
from bs4 import BeautifulSoup
import time

URL = "https://www.marukyu-koyamaen.co.jp/english/shop/products/1191040c1"
WEBHOOK = "https://discord.com/api/webhooks/1510995633694314636/x9RogpMnLhz4pOvp_on3_sxn73SW8iC8cKjeeqxiUarZZ6RL9uq5qNkclnKFQyYLCwyy"

last_state = None

def send(msg):
    try:
        requests.post(WEBHOOK, json={"content": msg}, timeout=10)
    except Exception as e:
        print("Discord error:", e)

def available(text):
    text = text.lower()
    return ("add to cart" in text) or ("in stock" in text)

while True:
    try:
        r = requests.get(
            URL,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=20
        )

        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text(" ", strip=True)

        current = available(text)

        # 初始化狀態
        if last_state is None:
            last_state = current

        # 從缺貨 → 有貨
        if current and not last_state:
            send("🍵 小山園補貨通知！\nIsuzu 40g 已可購買\n" + URL)

        last_state = current

    except Exception as e:
        print("error:", e)

    time.sleep(60)
