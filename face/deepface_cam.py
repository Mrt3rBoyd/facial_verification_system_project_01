import os
import cv2
from deepface import DeepFace

class FaceRecognitionSystem:
    def __init__(self, facial_data_dir):
        self.facial_data_dir = facial_data_dir

    # ============================================================
    # Compare live frame with the stored face (DeepFace)
    # ============================================================
    def recognize_face(self, frame, target_username):
        try:
            # path to user's stored face
            target_face_path = os.path.join(self.facial_data_dir, f"{target_username}.jpg")

            if not os.path.exists(target_face_path):
                print(f"No stored face found for user: {target_username}")
                return "Unknown"

            # Save current frame to temporary file because DeepFace requires images
            temp_path = "temp_live_frame.jpg"
            cv2.imwrite(temp_path, frame)

            # ==============================
            # DeepFace Verification
            # ==============================
            result = DeepFace.verify(
                img1_path=temp_path,
                img2_path=target_face_path,
                model_name="Facenet512",
                enforce_detection=False
            )

            # DeepFace returns distance score
            if result["verified"]:
                print("Face Found")  # You requested this message
                return target_username

            else:
                print("Face does not match")
                return "Unknown"

        except Exception as e:
            print("Error during face recognition:", str(e))
            return "Unknown"
