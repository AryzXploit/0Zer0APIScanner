import os
import getpass
import json
import sys
import time
import subprocess
from termcolor import colored

DB_FILE = "users.json"
SESSION_FILE = "session.txt"
WS_SCRIPT = "ws.py"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register():
    users = load_users()
    username = input(colored("🔑 Masukkan username: ", "yellow")).strip()
    if username in users:
        print(colored("❌ Username sudah terdaftar!", "red"))
        return
    password = getpass.getpass(colored("🔒 Masukkan password: ", "yellow")).strip()
    users[username] = password
    save_users(users)
    print(colored("✅ Registrasi berhasil! Silakan login.", "green"))

def login():
    users = load_users()
    username = input(colored("👤 Masukkan username: ", "yellow")).strip()
    password = getpass.getpass(colored("🔑 Masukkan password: ", "yellow")).strip()
    
    if username in users and users[username] == password:
        with open(SESSION_FILE, "w") as f:
            f.write(username)
        print(colored(f"🎉 Login berhasil! Selamat datang, {username} ✨", "green"))
        time.sleep(2)
        subprocess.run(["python3", WS_SCRIPT])
    else:
        print(colored("❌ Username atau password salah!", "red"))

def reset_password():
    users = load_users()
    username = input(colored("🔄 Masukkan username untuk reset password: ", "yellow")).strip()
    if username not in users:
        print(colored("❌ Username tidak ditemukan!", "red"))
        return
    new_password = getpass.getpass(colored("🔐 Masukkan password baru: ", "yellow")).strip()
    users[username] = new_password
    save_users(users)
    print(colored("✅ Password berhasil direset! Silakan login kembali.", "green"))

def main():
    clear_screen()
    print(colored("🔹 [1] Login", "cyan"))
    print(colored("🔹 [2] Register", "cyan"))
    print(colored("🔹 [3] Reset Password", "cyan"))
    choice = input(colored("📌 Pilih opsi (1-3): ", "yellow")).strip()
    
    if choice == "1":
        login()
    elif choice == "2":
        register()
    elif choice == "3":
        reset_password()
    else:
        print(colored("❌ Opsi tidak valid!", "red"))

if __name__ == "__main__":
    main()
