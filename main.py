import requests
from bs4 import BeautifulSoup
import json
import os

WEBHOOK = "https://discord.com/api/webhooks/1510995633694314636/x9RogpMnLhz4pOvp_on3_sxn73SW8iC8cKjeeqxiUarZZ6RL9uq5qNkclnKFQyYLCwyy"

PRODUCTS = {
    "Aoarashi": "https://www.marukyu-koyamaen.co.jp/english/shop/products/1141020c1",
    "Wako": "https://www.marukyu-koyamaen.co.jp/english/shop/products/1161020c1",
    "Isuzu": "https://www.marukyu-koyamaen.co.jp/english/shop/products/1191040c1",
    "Unkaku": "https://www.marukyu-koyamaen.co.jp/english/shop/products/11a1040c1"
}

STATE_FILE = "state.json"

def send(msg):
    try:
        requests.post(WEBHOOK, json={"content": msg}, timeout=10)
    except Exception as e:
        print("Discord error:", e)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def check_stock(url):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(" ", strip=True).lower()

    keyword = ("add to cart" in text or "in stock" in text)
    sold_out = ("sold out" in text or "out of stock" in text)
    has_form = soup.select_one("form") is not None

    return (keyword or has_form) and not sold_out

# 讀取上次狀態
state = load_state()

for name, url in PRODUCTS.items():
    current = check_stock(url)
    last = state.get(name, False)

    # 只在「無貨 → 有貨」通知
    if current and not last:
        send(f"🍵 小山園補貨通知！\n{name} 可購買\n{url}")

    state[name] = current

save_state(state)

print(state)
