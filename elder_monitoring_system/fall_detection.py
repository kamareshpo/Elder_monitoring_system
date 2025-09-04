import cv2
import mediapipe as mp
import time
from sos_alert import send_sos

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

def detect_fall(get_frame):
    print("📉 Fall Detection Started")
    fall_triggered = False
    fall_cooldown = 10  # seconds
    last_sos_time = 0

    while True:
        frame = get_frame()
        if frame is None:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb)

        if result.pose_landmarks:
            lm = result.pose_landmarks.landmark
            h, w, _ = frame.shape

            # Get Y positions of important parts
            nose_y = lm[mp_pose.PoseLandmark.NOSE].y
            hip_y = lm[mp_pose.PoseLandmark.LEFT_HIP].y

            # Convert to pixel height
            head_pos = int(nose_y * h)
            hip_pos = int(hip_y * h)

            # Heuristic fall detection: head or hip is very low (i.e. lying)
            if head_pos > h * 0.85 or hip_pos > h * 0.85:
                if time.time() - last_sos_time > fall_cooldown:
                    cv2.imwrite("fall.jpg", frame)
                    send_sos("💥 Fall Detected (lying position)! SOS Triggered.", photo_path="fall.jpg")
                    last_sos_time = time.time()

        time.sleep(0.3)  # reduce CPU usage
