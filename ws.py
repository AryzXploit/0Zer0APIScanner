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
███████╗███████╗██████╗  ██████╗  █████╗ ██████╗
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

TOOLS = {
    "gau": "go install github.com/lc/gau/v2/cmd/gau@latest",
    "waybackurls": "go install github.com/tomnomnom/waybackurls@latest",
    "katana": "go install github.com/projectdiscovery/katana/cmd/katana@latest",
    "subjs": "go install github.com/lc/subjs@latest",
    "trufflehog": "pip install trufflehog",
    "gitleaks": "go install github.com/gitleaks/gitleaks/v8@latest"
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return f.read().strip()
    return None

def run_command(command, output_file=None):
    """Jalankan command & simpan output ke file jika diberikan."""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if output_file:
            with open(output_file, "w") as f:
                f.write(result.stdout)
        return result.stdout.strip()
    except Exception as e:
        print(colored(f"[X] Error: {e}", "red"))
        return ""

def scan():
    clear_screen()
    print(colored(f'"{random.choice(QUOTES)}"', "cyan"))
    print(colored("0Zer0APIScanner - API Recon & Secret Detection", "cyan"))

    domain = input(colored("Masukkan Domain Target: ", "yellow"))
    folder_path = os.path.join(os.getcwd(), domain)
    os.makedirs(folder_path, exist_ok=True)

    print(colored("Pilih jenis scanning:", "yellow"))
    print(colored("1. API Recon (Gau, Waybackurls, ParamSpider)", "cyan"))
    print(colored("2. JavaScript Analysis (LinkFinder, subjs, katana)", "cyan"))
    print(colored("3. Secret Finder (SecretFinder, TruffleHog, GitLeaks)", "cyan"))
    print(colored("4. Full API Scan (BETA TEST)", "cyan"))

    choice = input(colored("Pilih mode (1-4): ", "yellow"))

    tasks = []

    if choice == "1":
        tasks.append(threading.Thread(target=run_command, args=(f"gau {domain} | tee {folder_path}/api_endpoints.txt",)))
        tasks.append(threading.Thread(target=run_command, args=(f"waybackurls {domain} | tee -a {folder_path}/api_endpoints.txt",)))
    elif choice == "2":
        tasks.append(threading.Thread(target=run_command, args=(f"katana -u https://{domain} -jc -o {folder_path}/js_files.txt",)))
        tasks.append(threading.Thread(target=run_command, args=(f"subjs -i {folder_path}/js_files.txt -o {folder_path}/js_api_endpoints.txt",)))
    elif choice == "3":
        tasks.append(threading.Thread(target=run_command, args=(f"trufflehog --regex --entropy=True --max_depth 10 {domain} | tee -a {folder_path}/secrets.txt",)))
        tasks.append(threading.Thread(target=run_command, args=(f"gitleaks detect -s {domain} -r {folder_path}/git_leaks.txt",)))
    elif choice == "4":
        for task in [1, 2, 3]:
            scan()
    else:
        print(colored("[!] Mode belum tersedia!", "red"))
        return

    for task in tasks:
        task.start()
    for task in tasks:
        task.join()

    print(colored(f"[+] Scan selesai! Hasil disimpan di {folder_path}", "green"))

def main():
    clear_screen()
    username = load_session()
    if not username:
        print(colored("[X] Access Denied! Silakan login terlebih dahulu.", "red"))
        print(colored("Jalankan `python3 login.py` untuk masuk.", "yellow"))
        sys.exit(1)

    print(colored(ASCII_ART, "cyan"))
    print(WARNING_TEXT)
    print(colored(f"[✔] Selamat datang, {username}!", "green"))
    print(colored("Memulai 0Zer0APIScanner...", "blue"))
    scan()

if __name__ == "__main__":
    main()
