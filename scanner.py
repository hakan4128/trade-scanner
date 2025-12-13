import requests
import datetime

# === AYARLAR ===
BOT_TOKEN = "BURAYA_BOT_TOKEN"
CHAT_ID = "BURAYA_CHAT_ID"

# Basit örnek hisse listesi (şimdilik)
WATCHLIST = ["NVDA", "TSLA", "AAPL"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

def run_scanner():
    now = datetime.datetime.now().strftime("%H:%M")
    msg = "📊 A+ Scanner Çalıştı\n"
    msg += f"⏰ Saat: {now}\n\n"

    for symbol in WATCHLIST:
        msg += f"• {symbol} → İzleniyor\n"

    send_telegram(msg)

if __name__ == "__main__":
    run_scanner()
