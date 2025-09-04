import cv2

def night_camera():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Night Vision: Cannot open camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("🌙 Night Vision Mode", gray)

        if cv2.waitKey(1) & 0xFF == ord('n'):
            print("🔴 Exiting Night Vision Mode")
            break

    cap.release()
    cv2.destroyAllWindows()
