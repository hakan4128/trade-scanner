import requests
import datetime
import os
import xml.etree.ElementTree as ET

# Telegram bilgileri (Secrets'ten gelir)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Takip edilecek hisseler (şimdilik manuel)
SYMBOLS = ["NVDA", "TSLA", "AAPL"]

def get_today_news(symbol):
    url = f"https://news.google.com/rss/search?q={symbol}+stock&hl=en-US&gl=US&ceid=US:en"

    r = requests.get(url)
    root = ET.fromstring(r.content)

    for item in root.iter("item"):
        title = item.find("title").text
        return title  # ilk haberi al

    return None

def translate_to_tr(text):
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "en",
        "tl": "tr",
        "dt": "t",
        "q": text
    }
    r = requests.get(url, params=params)
    return r.json()[0][0][0]

def analyze_news(text):
    negative = ["offering", "dilution", "investigation", "lawsuit"]
    fake = ["reddit", "social media", "short squeeze"]

    t = text.lower()

    for w in negative:
        if w in t:
            return "🔴 Negatif / Riskli"

    for w in fake:
        if w in t:
            return "⚠️ Fake Pump Riski"

    return "🟢 Pozitif / Gerçek Katalist"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, json=data)

def run():
    for sym in SYMBOLS:
        news = get_today_news(sym)

        if not news:
            send_telegram(f"⚠️ {sym} için haber bulunamadı")
            continue

        tr_news = translate_to_tr(news)
        analysis = analyze_news(news)

        message = f"""
📊 {sym}

📰 Son Haber:
{tr_news}

🧠 Yorum:
{analysis}
"""
        send_telegram(message)

run()
send_telegram("🚨 scanner.py çalıştı")
