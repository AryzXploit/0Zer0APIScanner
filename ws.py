import os
import getpass
import subprocess
import time
import sys
import random
import threading
from termcolor import colored
from shutil import which

LOCKFILE = "/var/tmp/.cache_sys_zer0api.lock"
LOCK_DURATION = 300  # 5 menit

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

def check_lock():
    if os.path.exists(LOCKFILE):
        with open(LOCKFILE, "r") as f:
            lock_time = int(f.read().strip())
        current_time = int(time.time())

        if current_time - lock_time < LOCK_DURATION:
            remaining = LOCK_DURATION - (current_time - lock_time)
            print(colored(f"[X] Tools terkunci! Tunggu {remaining} detik.", "red"))
            exit(1)
        else:
            os.remove(LOCKFILE)

def install_tools():
    """Cek dan install semua tools yang dibutuhkan."""
    print(colored("[+] Mengecek dependencies...", "cyan"))
    for tool, install_cmd in TOOLS.items():
        if which(tool) is None:
            print(colored(f"[!] {tool} tidak ditemukan, menginstall...", "yellow"))
            subprocess.run(install_cmd, shell=True)
        else:
            print(colored(f"[✔] {tool} sudah terinstall!", "green"))

def animate_verification():
    sys.stdout.write(colored("Verifying password", "cyan"))
    sys.stdout.flush()
    for _ in range(3):
        time.sleep(1)
        sys.stdout.write(colored(".", "cyan"))
        sys.stdout.flush()
    print(colored(" Done!", "green"))
    time.sleep(1)

def login():
    check_lock()
    password = "user"
    attempts = 3

    while attempts > 0:
        user_input = getpass.getpass(colored("Masukkan Password: ", "yellow"))
        if user_input == password:
            animate_verification()
            print(colored("Verification successful! Welcome home, sir", "cyan"))
            time.sleep(2)
            break
        else:
            attempts -= 1
            print(colored(f"Password salah! Kesempatan tersisa: {attempts}", "red"))
            if attempts == 0:
                print(colored("Terlalu banyak percobaan! Tools terkunci 5 menit!", "red"))
                with open(LOCKFILE, "w") as f:
                    f.write(str(int(time.time())))
                exit(1)
    clear_screen()

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
        tasks.append(threading.Thread(target=run_command, args=(f"python3 ParamSpider.py --domain {domain} --output {folder_path}/api_parameters.txt",)))
    elif choice == "2":
        tasks.append(threading.Thread(target=run_command, args=(f"katana -u https://{domain} -jc -o {folder_path}/js_files.txt",)))
        tasks.append(threading.Thread(target=run_command, args=(f"subjs -i {folder_path}/js_files.txt -o {folder_path}/js_api_endpoints.txt",)))
        tasks.append(threading.Thread(target=run_command, args=(f"python3 linkfinder.py -i {folder_path}/js_files.txt -o cli | tee {folder_path}/js_links.txt",)))
    elif choice == "3":
        tasks.append(threading.Thread(target=run_command, args=(f"python3 SecretFinder.py -i {folder_path}/js_files.txt -o cli | tee {folder_path}/secrets.txt",)))
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
    install_tools()
    login()
    scan()

if __name__ == "__main__":
    main()
