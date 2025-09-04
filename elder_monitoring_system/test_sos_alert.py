import requests

TOKEN = "7899915167:AAFWxl9JXP2dqrDEjJXFvzeu1933P1UzyTk"
CHAT_ID = "1114449056"

message = "🚨 Test SOS Alert from Olaibs_bot — monitoring system is working!"

def send_test_message():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    r = requests.post(url, data=payload)
    print("✅ Sent!" if r.status_code == 200 else f"❌ Failed: {r.text}")

send_test_message()
