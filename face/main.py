# main.py
import os
import getpass
import cv2
from deepface_cam import FaceRecognitionSystem
import time

USER_FILE = "user_data.txt"
facial_data_DIR = "facial_data"
PROCESS_EVERY = 5

#=============================================================
# User Functions

def register():
    username = input("Enter new username: ").strip()
    face_path = os.path.join(facial_data_DIR, f"{username}.jpg")

    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            for line in f:
                if username == line.strip().split(",")[0]:
                    print("⚠️Username already exists!⚠️")
                    return

    password = getpass.getpass("Enter password: ").strip()

    # Capture face automatically
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("⚠️Cannot open webcam⚠️")
        return

    print("Look at the camera. Press 'c' to capture your face.")
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        cv2.imshow("Capture Face", frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            if not os.path.exists(facial_data_DIR):
                os.makedirs(facial_data_DIR)
            cv2.imwrite(face_path, frame)
            print(f"Face saved as {face_path}")
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save username/password
    with open(USER_FILE, "a") as f:
        f.write(f"{username},{password}\n")
    print(f"Registered: {username}")


def login():
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ").strip()
    face_path = os.path.join(facial_data_DIR, f"{username}.jpg")

    if not os.path.exists(USER_FILE):
        print("💀No users found")
        return None
    if not os.path.exists(face_path):
        print(f"💀No data found for {username} in the system")
        return None

    with open(USER_FILE, "r") as f:
        for line in f:
            stored_user, stored_pass = line.strip().split(",")
            if stored_user == username and stored_pass == password:
                print(f"Password correct: {username}")
                return username

    print("💀Invalid login")
    return None


# =======================================================
# Face Recognition

def face_login(username):
    fr_system = FaceRecognitionSystem(facial_data_DIR)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("⚠️Cannot open webcam")
        return False

    print("Show your face to login. Press 'q' to quit.")
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        frame_count += 1

        if frame_count % PROCESS_EVERY == 0:
            name = fr_system.recognize_face(frame, username)

        else:
            name = "Processing..."

        cv2.putText(frame, f"Detected: {name}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0) if name.lower() == username.lower() else (0,0,255), 2)
        cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0]-20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1)
        cv2.imshow("Face Login", frame)

        if name.lower() == username.lower():
            print(f"Face recognized! {username} is successfully logged in!")
            cap.release()
            cv2.destroyAllWindows()
            return True

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("💀Face login failed.")
    return False

#=====================================================================
### the time count down founction
def face_login(username):
    fr_system = FaceRecognitionSystem(facial_data_DIR)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open webcam")
        return False

    print("Show your face to login. You have 5 seconds...")
    frame_count = 0
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        frame_count += 1

        # 5 second timeout
        elapsed = time.time() - start_time
        if elapsed > 5:
            print("Time is up! loggin failed.")
            break

        # Only process every N frames
        if frame_count % PROCESS_EVERY == 0:
            name = fr_system.recognize_face(frame, username)
        else:
            name = "Processing..."

        # Show remaining time on screen
        remaining = max(0, 5 - int(elapsed))
        cv2.putText(frame, f"Time left: {remaining}s", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.putText(frame, f"Detected: {name}", (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0) if name.lower() == username.lower() else (0,0,255), 2)

        cv2.imshow("Face Login", frame)

        # If face matched earlier
        if name.lower() == username.lower():
            print(f"Face recognized! {username} successfully logged in!")
            cap.release()
            cv2.destroyAllWindows()
            return True

        # Allow quit manually
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("❌ Face login failed. ❌")
    return False



#================================================================
# Main CLI

def main():
    while True:

        print("⠀⠀⠀⠀⠀⣀⣀⣀⣀⣠⣤⣤⣄⣀⣀⣀⣀")
        print("⢀⣠⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣄⡀")
        print("⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷")
        print("⣿⣿⣿⡿⠛⠉⠉⠙⠿⣿⣿⣿⣿⠿⠋⠉⠉⠛⢿⣿⣿⣿")
        print("⣿⣿⣿⣶⣿⣿⣿⣦⠀⢘⣿⣿⡃⠀⣴⣿⣿⣿⣶⣿⣿⣿")
        print("⣿⣿⣿⣏⠉⠀⠈⣙⣿⣿⣿⣿⣿⣿⣋⠁⠀⠉⣹⣿⣿⣿")
        print("⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
        print("⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
        print("⢸⣿⣿⣎⠻⣿⣿⣿⣿⡿⠋⠙⢿⣿⣿⣿⣿⠟⣱⣿⣿⡇")
        print("⠀⢿⣿⣿⣧⠀⠉⠉⠉⠀⢀⡀⠀⠉⠉⠉⠀⣼⣿⣿⡿")
        print("⠀⠈⢻⣿⣿⣷⣶⣶⣶⣶⣿⣿⣶⣶⣶⣶⣾⣿⣿⡟⠁")
        print("⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⠉⠉⣿⣿⣿⣿⣿⣿⠏")
        print("⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⠟⠁")
        print("⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣦⣴⡿⠟⠋")
        
        print("Menu")
        print("[ 1 ]. Register")
        print("[ 2 ]. Login")
        print("[ 3 ]. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            username = login()
            if username:
                face_login(username)
        elif choice == "3":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
