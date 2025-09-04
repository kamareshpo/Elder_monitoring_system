
# elder_monitoring_system/main.py

from threading import Thread
import cv2
import monitor_motion
import gesture_sos
import fall_detection
import night_vision
import time

shared_frame = None
capture_running = True

# Shared camera capture loop
def camera_stream():
    global shared_frame, capture_running
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Shared Camera: Cannot open camera.")
        capture_running = False
        return
    while capture_running:
        ret, frame = cap.read()
        if not ret:
            print("❌ Shared Camera: Frame grab failed.")
            break
        shared_frame = frame
        time.sleep(0.01)
    cap.release()

# Worker functions use shared_frame
def run_motion():
    while capture_running:
        monitor_motion.detect_motion(lambda: shared_frame)

def run_gesture():
    gesture_sos.detect_gesture(lambda: shared_frame)

def run_fall():
    while capture_running:
        fall_detection.detect_fall(lambda: shared_frame)


def run_night():
    while capture_running:
        night_vision.night_camera(lambda: shared_frame)

def run_live_view():
    global shared_frame
    while True:
        frame = shared_frame
        if frame is not None:
            cv2.imshow("Live CCTV Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🔴 Stopping System")
            break
    global capture_running
    capture_running = False
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Start camera stream
    Thread(target=camera_stream).start()

    # Start detection modules
    Thread(target=run_motion).start()
    Thread(target=run_gesture).start()
    Thread(target=run_fall).start()
    Thread(target=run_night).start()
    Thread(target=run_live_view).start()

    print("🟢 Elder Monitoring System Running... Press 'q' to stop.")
