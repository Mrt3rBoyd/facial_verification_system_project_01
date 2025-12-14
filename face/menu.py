# menu.py
import os
import getpass

USER_FILE = "user_data.txt"

def register():
    username = input("Enter new username: ").strip()
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            for line in f:
                if username == line.strip().split(",")[0]:
                    print("Username exists!")
                    return
    password = getpass.getpass("Enter password: ").strip()
    with open(USER_FILE, "a") as f:
        f.write(f"{username},{password}\n")
    print(f"Registered: {username}")
    

def login():
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ").strip()
    if not os.path.exists(USER_FILE):
        print("No users found")
        return None
    with open(USER_FILE, "r") as f:
        for line in f:
            stored_user, stored_pass = line.strip().split(",")
            if stored_user == username and stored_pass == password:
                print(f"Password correct: {username}")
                return username
    print("Invalid login")
    return None

def menu_process(user_queue):
    while True:
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
                user_queue.put(username)  # send to camera terminal
        elif choice == "3":
            print("Exiting menu")
            user_queue.put("EXIT")
            break
        else:
            print("Invalid choice")
