print("### NEW VERSION V2 ###")
import requests
import os
import xml.etree.ElementTree as ET

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SYMBOLS = ["NVDA"]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

def get_news(symbol):
    url = f"https://news.google.com/rss/search?q={symbol}+stock&hl=en-US&gl=US&ceid=US:en"
    r = requests.get(url)
    root = ET.fromstring(r.content)

    for item in root.iter("item"):
        return item.find("title").text
    return None

def translate_tr(text):
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

def score_and_grade(text):
    t = text.lower()
    score = 0

    positive = ["beats", "strong", "record", "growth", "surge"]
    negative = ["offering", "dilution", "investigation", "lawsuit"]

    if any(w in t for w in positive):
        score += 50
    if not any(w in t for w in negative):
        score += 50

    if score >= 80:
        grade = "A+"
    elif score >= 60:
        grade = "A"
    else:
        grade = "İzleme Dışı"

    return score, grade

def run():
    for sym in SYMBOLS:
        news = get_news(sym)

        if not news:
            send_telegram("Haber bulunamadı")
            return

        news_tr = translate_tr(news)
        score, grade = score_and_grade(news)

        msg = f"""
📊 {sym} — {grade}

📰 Haber:
{news_tr}

⭐ Skor: {score}/100
"""
         send_telegram("🆕 YENİ A/A+ SÜRÜMÜ ÇALIŞIYOR")

run()
# temp