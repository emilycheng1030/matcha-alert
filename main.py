import requests
from bs4 import BeautifulSoup

URL = "https://www.marukyu-koyamaen.co.jp/english/shop/products/1191040c1"
WEBHOOK = "https://discord.com/api/webhooks/1510995633694314636/x9RogpMnLhz4pOvp_on3_sxn73SW8iC8cKjeeqxiUarZZ6RL9uq5qNkclnKFQyYLCwyy"

def send(msg):
    try:
        requests.post(WEBHOOK, json={"content": msg}, timeout=10)
    except Exception as e:
        print("Discord error:", e)

def check_stock(soup, text):
    text = text.lower()

    # ① 基本關鍵字判斷
    keyword_available = (
        "add to cart" in text or
        "in stock" in text
    )

    # ② 更重要：是否有購物表單（通常有貨才會出現）
    has_cart_form = soup.select_one("form") is not None

    # ③ 是否明確寫 sold out
    sold_out = "sold out" in text or "out of stock" in text

    # 判斷邏輯（核心）
    return (keyword_available or has_cart_form) and not sold_out

try:
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(" ", strip=True)

    if check_stock(soup, text):
        send("🍵 小山園補貨通知！\nIsuzu 40g 可能可購買\n" + URL)
    else:
        print("目前無貨")

except Exception as e:
    print("error:", e)
