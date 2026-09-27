import cv2

def open_camera():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return "I couldn't open the camera."

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow("Nispara Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    return "Camera closed."