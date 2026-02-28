import requests
import os

# ====== 填入你的 Bot Token ======
TOKEN = "8680917385:AAGom7M4Mjt8lcti-nFPDdH6oMOZDMaL3yQ"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# ====== 存储 update_id 文件 ======
LAST_UPDATE_FILE = "last_update.txt"


# ---------- 发送消息 ----------
def send_message(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        response = requests.post(
            f"{BASE_URL}/sendMessage",
            json=payload,
            timeout=10
        )
        return response.json()
    except Exception as e:
        print("发送失败:", e)
        return None


# ---------- 获取更新（禁止长轮询，防止超时） ----------
def get_updates(offset=None):
    url = f"{BASE_URL}/getUpdates"

    params = {
        "timeout": 0   # 关键：立即返回
    }

    if offset:
        params["offset"] = offset

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )
        return response.json()
    except Exception as e:
        print("获取更新失败:", e)
        return {"result": []}


# ---------- 读取最后 update_id ----------
def get_last_update_id():
    if not os.path.exists(LAST_UPDATE_FILE):
        return None
    with open(LAST_UPDATE_FILE, "r") as f:
        return int(f.read().strip())


# ---------- 保存 update_id ----------
def save_last_update_id(update_id):
    with open(LAST_UPDATE_FILE, "w") as f:
        f.write(str(update_id))


# ---------- 业务逻辑 ----------
def handle_message(chat_id, text):
    parts = text.split()

    if text == "/start":
        send_message(chat_id, "小管家上线了 👋")

    elif parts[0] == "/setcity" and len(parts) > 1:
        city = parts[1]
        send_message(chat_id, f"城市已设置为 {city}")

    elif parts[0] == "/settransport" and len(parts) > 1:
        transport = parts[1]
        send_message(chat_id, f"出行方式已设置为 {transport}")

    else:
        send_message(chat_id, "指令不正确")


# ---------- 主程序 ----------
if __name__ == "__main__":

    last_update_id = get_last_update_id()

    data = get_updates(last_update_id)

    for update in data["result"]:
        update_id = update["update_id"]
        message = update.get("message")

        if not message:
            continue

        chat_id = str(message["chat"]["id"])
        text = message.get("text", "")

        print("收到消息:", text)

        handle_message(chat_id, text)

        save_last_update_id(update_id + 1)