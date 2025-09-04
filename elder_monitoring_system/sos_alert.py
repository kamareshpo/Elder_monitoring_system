import requests
from utils.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def send_sos(message, photo_path=None, video_path=None):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": TELEGRAM_CHAT_ID, "text": message}
    )

    if photo_path:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto",
            data={"chat_id": TELEGRAM_CHAT_ID},
            files={"photo": open(photo_path, "rb")}
        )

    if video_path:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVideo",
            data={"chat_id": TELEGRAM_CHAT_ID},
            files={"video": open(video_path, "rb")}
        )
