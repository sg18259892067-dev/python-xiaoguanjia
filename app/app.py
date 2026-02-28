from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# ---------- 发送消息 ----------
def send_message(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(f"{BASE_URL}/sendMessage", json=payload)


# ---------- Webhook 接收 ----------
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "小管家 Pro 已上线 🚀")

        elif text.startswith("/setcity"):
            parts = text.split()
            if len(parts) > 1:
                send_message(chat_id, f"城市已设置为 {parts[1]}")

        elif text.startswith("/settransport"):
            parts = text.split()
            if len(parts) > 1:
                send_message(chat_id, f"出行方式已设置为 {parts[1]}")

        else:
            send_message(chat_id, "指令不正确")

    return "ok"