import os
import getpass
import subprocess
import time
import sys
import json
import threading
import random
from termcolor import colored
from shutil import which

DB_FILE = "users.json"
LOCKFILE = "/var/tmp/.cache_sys_zer0api.lock"
LOCK_DURATION = 300  # 5 menit
SESSION_FILE = "session.txt"

ASCII_ART = """
███████╗███████╗██████╗  ██████╗  ██████╗ ██████╗
██╔════╝██╔════╝██╔══██╗██╔════╝ ██╔══██╗██╔══██╗
███████╗█████╗  ██████╔╝██║  ███╗███████║██████╔╝
╚════██║██╔══╝  ██╔══██╗██║   ██║██╔══██║██╔══██╗
███████║███████╗██████╔╝╚██████╔╝██║  ██║██║  ██║
╚══════╝╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
"""

WARNING_TEXT = colored("""
[WARNING]
Jangan gunakan alat ini untuk tujuan ilegal!
Gunakan dengan tanggung jawab dan etika yang benar.
""", "red", attrs=["bold"])

QUOTES = [
    "Keamanan API adalah prioritas utama dalam dunia cybersecurity.",
    "Jangan pernah menyimpan kredensial API dalam kode sumber.",
    "Semakin dalam kamu menggali, semakin banyak yang kamu temukan.",
    "Berpikirlah seperti penyerang untuk menjadi pembela yang lebih baik.",
    "Setiap API memiliki kelemahan, tugas kita menemukannya sebelum yang lain.",
    "0Zer0APIScanner – Mendeteksi yang tersembunyi, mengamankan yang rentan."
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return f.read().strip()
    return None

def check_tools(tools):
    missing_tools = [tool for tool in tools if not which(tool)]
    if missing_tools:
        print(colored(f"[!] Alat berikut tidak ditemukan: {', '.join(missing_tools)}", "red"))
        install = input(colored("[?] Install otomatis? (y/n): ", "yellow")).strip().lower()
        if install == "y":
            for tool in missing_tools:
                subprocess.run(f"sudo apt install -y {tool}", shell=True)
        else:
            sys.exit(1)

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(colored(f"[!] Error saat menjalankan: {command}", "red"))
        print(colored(str(e), "red"))

def is_locked():
    if os.path.exists(LOCKFILE):
        lock_time = os.path.getmtime(LOCKFILE)
        if time.time() - lock_time < LOCK_DURATION:
            return True
    return False

def create_lock():
    with open(LOCKFILE, "w") as f:
        f.write(str(time.time()))

def remove_lock():
    if os.path.exists(LOCKFILE):
        os.remove(LOCKFILE)

def clear_cache():
    remove_lock()
    print(colored("[✔] Cache berhasil dibersihkan!", "green"))

def scan():
    if is_locked():
        print(colored("[X] Scanner sedang berjalan, tunggu beberapa saat...", "red"))
        sys.exit(1)
    
    create_lock()
    clear_screen()
    print(colored(ASCII_ART, "cyan"))
    print(colored(f'"{random.choice(QUOTES)}"', "cyan"))
    print(colored("0Zer0APIScanner - API Recon & Secret Detection", "cyan"))

    domain = input(colored("Masukkan Domain Target: ", "yellow")).strip()
    folder_path = os.path.join("results", domain)
    os.makedirs(folder_path, exist_ok=True)

    print(colored("Pilih jenis scanning:", "yellow"))
    print(colored("1. API Recon (Gau, Waybackurls, ParamSpider)", "cyan"))
    print(colored("2. JavaScript Analysis (LinkFinder, subjs, katana)", "cyan"))
    print(colored("3. Secret Finder (SecretFinder, TruffleHog)", "cyan"))
    print(colored("4. Full API Scan (BETA TEST)", "cyan"))
    print(colored("5. Clear Cache", "cyan"))

    choice = input(colored("Pilih mode (1-5): ", "yellow")).strip()
    
    if choice == "5":
        clear_cache()
        return
    
    tasks = []
    if choice == "1":
        check_tools(["gau", "waybackurls", "paramspider"])
        tasks.append(threading.Thread(target=run_command, args=(f"gau {domain} | tee {folder_path}/api_endpoints.txt",)))
        tasks.append(threading.Thread(target=run_command, args=(f"waybackurls {domain} | tee -a {folder_path}/api_endpoints.txt",)))
        tasks.append(threading.Thread(target=run_command, args=(f"paramspider --domain {domain} --output {folder_path}/params.txt",)))
    elif choice == "2":
        check_tools(["katana", "subjs", "linkfinder"])
        tasks.append(threading.Thread(target=run_command, args=(f"katana -u https://{domain} -jc -o {folder_path}/js_files.txt",)))
        tasks.append(threading.Thread(target=run_command, args=(f"subjs -i {folder_path}/js_files.txt | tee {folder_path}/js_api_endpoints.txt",)))
        tasks.append(threading.Thread(target=run_command, args=(f"python3 ~/LinkFinder/linkfinder.py -i {folder_path}/js_files.txt -o cli",)))
    elif choice == "3":
        check_tools(["trufflehog", "secretfinder"])
        tasks.append(threading.Thread(target=run_command, args=("cat | while read url ; do python3 ~/SecretFinder/SecretFinder.py -i $url -o cli ;done",)))
        tasks.append(threading.Thread(target=run_command, args=(f"trufflehog --regex --entropy=True --max_depth 10 {domain} | tee -a {folder_path}/secrets.txt",)))
    
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()

    remove_lock()
    print(colored(f"[+] Scan selesai! Hasil disimpan di {folder_path}", "green"))

def main():
    if "--clear-cache" in sys.argv:
        clear_cache()
        sys.exit(0)
    scan()

if __name__ == "__main__":
    main()
