import cv2
import mediapipe as mp
import time
from sos_alert import send_sos

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

def record_video(get_frame, duration=10, filename="gesture_sos_video.avi"):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
    start_time = time.time()
    while time.time() - start_time < duration:
        frame = get_frame()
        if frame is not None:
            out.write(frame)
    out.release()

def detect_gesture(get_frame):
    print("📸 Gesture SOS Detection started.")
    last_chest_hand_time = None
    sos_sent = False

    while True:
        frame = get_frame()
        if frame is None:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb)

        if result.pose_landmarks:
            lm = result.pose_landmarks.landmark
            h, w, _ = frame.shape
            nose_y = lm[mp_pose.PoseLandmark.NOSE].y

            left_wrist = lm[mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = lm[mp_pose.PoseLandmark.RIGHT_WRIST]
            left_y = left_wrist.y
            right_y = right_wrist.y

            # Draw skeleton and keypoints
            mp_draw.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Backup gesture 1: both hands up
            if left_y < nose_y and right_y < nose_y:
                trigger_sos("🙋 SOS: Both hands raised", frame, get_frame)
                break

            # Backup gesture 2: left hand up (wave detection not deep here)
            elif left_y < nose_y and right_y > nose_y:
                trigger_sos("👋 SOS: Left hand waving", frame, get_frame)
                break

            # Backup gesture 3: right hand held at chest for 3 seconds
            elif abs(right_wrist.x - 0.5) < 0.1 and abs(right_wrist.y - 0.5) < 0.1:
                if last_chest_hand_time is None:
                    last_chest_hand_time = time.time()
                elif time.time() - last_chest_hand_time > 3:
                    trigger_sos("✋ SOS: Hand held at chest", frame, get_frame)
                    break
            else:
                last_chest_hand_time = None

def trigger_sos(message, frame, get_frame):
    print(f"🚨 Gesture SOS Triggered: {message}")
    photo_path = "gesture_sos_photo.jpg"
    video_path = "gesture_sos_video.avi"

    cv2.imwrite(photo_path, frame)
    record_video(get_frame, duration=10, filename=video_path)
    send_sos(message, photo_path=photo_path, video_path=video_path)
