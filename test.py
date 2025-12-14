import os
import requests

token = os.getenv("BOT_TOKEN")
chat = os.getenv("CHAT_ID")

url = f"https://api.telegram.org/bot{token}/sendMessage"
data = {
    "chat_id": chat,
    "text": "✅ Test başarılı"
}

requests.post(url, json=data)
