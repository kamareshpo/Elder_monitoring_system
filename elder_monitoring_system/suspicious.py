# suspicious.py
import cv2
import time
from datetime import datetime
from sos_alert import send_sos

def record_video(file_path="suspicious.avi", duration=10):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(file_path, fourcc, 20.0, (640,480))

    start_time = time.time()
    while (int(time.time() - start_time) < duration):
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            cv2.imshow('Recording', frame)
            if cv2.waitKey(1) == ord('q'):
                break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return file_path

def suspicious_activity_detected():
    photo_path = "suspect.jpg"
    video_path = "suspicious.avi"
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    cv2.imwrite(photo_path, frame)
    cap.release()

    vid = record_video(video_path)
    send_sos("Suspicious Activity Detected!", photo_path, vid)
