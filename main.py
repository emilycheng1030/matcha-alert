import requests
from bs4 import BeautifulSoup

URL = "https://www.marukyu-koyamaen.co.jp/english/shop/products/1191040c1"
WEBHOOK = "https://discord.com/api/webhooks/1510995633694314636/x9RogpMnLhz4pOvp_on3_sxn73SW8iC8cKjeeqxiUarZZ6RL9uq5qNkclnKFQyYLCwyy"

def send(msg):
    requests.post(WEBHOOK, json={"content": msg})

r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
soup = BeautifulSoup(r.text, "html.parser")
text = soup.get_text(" ", strip=True).lower()

if "add to cart" in text or "in stock" in text:
    send("🍵 小山園補貨通知！\nIsuzu 40g 可購買\n" + URL)
