import cv2
import time
from datetime import datetime, timedelta
from sos_alert import send_sos
from utils.config import NO_MOVEMENT_THRESHOLD_HOURS

last_movement_time = datetime.now()
ALERT_THRESHOLD = timedelta(hours=NO_MOVEMENT_THRESHOLD_HOURS)

def detect_motion():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Motion Detection: Cannot open camera.")
        return

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    while True:
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            global last_movement_time
            last_movement_time = datetime.now()

        if datetime.now() - last_movement_time > ALERT_THRESHOLD:
            send_sos("🚨 No movement detected for 1 hour! SOS Triggered.")
            last_movement_time = datetime.now()

        frame1 = frame2
        ret, frame2 = cap.read()
        if not ret:
            break

    cap.release()
