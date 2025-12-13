import requests

def send_test_message():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": "✅ Trade Scanner çalışıyor. Test mesajı."
    }
    requests.post(url, json=payload)

send_test_message()
