# camera.py
import cv2
from deepface_cam import FaceRecognitionSystem

#facial_data
facial_data_folder = "facial_data"
process_every = 5

def camera_process(user_queue):
    fr_system = FaceRecognitionSystem(facial_data_folder)
    cap = cv2.VideoCapture(0)
    frame_count = 0
    current_user = None
    last_name = "Unknown"

    while True:
        if not user_queue.empty():
            msg = user_queue.get() # Check: Is the item we just got equal to the EXIT signal?
            if msg == "EXIT":
                break
            current_user = msg
            print(f"Start face login for {current_user}")

        ret, frame = cap.read()
        if not ret:
            continue

        frame_count += 1

        if current_user and frame_count % process_every == 0:
            last_name = fr_system.recognize_face(frame)
            if last_name.lower() == current_user.lower():
                print(f"{last_name} recognized! Login successful!")
                current_user = None  # reset after success

        cv2.putText(frame, f"Detected: {last_name}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0) if last_name != "Unknown" else (0,0,255), 2)
        cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0]-20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1)
        cv2.imshow("Face Login", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
