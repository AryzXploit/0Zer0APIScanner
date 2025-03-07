#!/bin/bash

# Warna untuk tampilan lebih keren
RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
MAGENTA='\033[1;35m'
RESET='\033[0m'

# Banner
clear
echo -e "${MAGENTA}"
echo "    ██████  ███████ ██████   ██████   ██████   █████▒"
echo "    ▒██    ▒ ██      ██   ██ ██    ██ ██    ██ ██   ██"
echo "    ▒████  ▒ █████   ██   ██ ██    ██ ██    ██ ██   ██"
echo "    ▒██    ▒ ██      ██   ██ ██    ██ ██    ██ ██   ██"
echo "    ▒██    ▒ ███████ ██████   ██████   ██████  ██████"
echo "    ======================================"
echo "    ||     Instalasi Recon Apikey       ||"
echo "    ||                                  ||"
echo "    ======================================"
echo -e "${RESET}"

# Deteksi sistem
if [ -d "/data/data/com.termux" ]; then
    OS="termux"
    PKG_MANAGER="pkg"
    echo -e "${CYAN}[+] Detected: Bocil Termux${RESET}"
else
    OS="linux"
    PKG_MANAGER="sudo apt"
    echo -e "${CYAN}[+] Detected: Linux Or Somelse${RESET}"
fi

install_tools() {
    echo -e "${CYAN}[+] Installing dependencies...${RESET}"
    $PKG_MANAGER update -y && $PKG_MANAGER install -y curl git python3 python3-pip jq unzip

    # Install Go
    if ! command -v go &> /dev/null; then
        echo -e "${CYAN}[+] Installing Go...${RESET}"
        curl -fsSL https://golang.org/dl/go1.21.5.linux-amd64.tar.gz | sudo tar -C /usr/local -xz
        echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> ~/.bashrc
        source ~/.bashrc
    else
        echo -e "${GREEN}[✔] Go udh keinstall!${RESET}"
    fi

    # Install ProjectDiscovery Tools
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

    # Install API Key Scanners
    echo -e "${CYAN}[+] Installing API Key scanning tools...${RESET}"
    git clone https://github.com/m4ll0k/SecretFinder.git $HOME/SecretFinder && pip install -r $HOME/SecretFinder/requirements.txt
    go install github.com/dxa4481/truffleHog@latest
    go install github.com/zricethezav/gitleaks/v8/cmd/gitleaks@latest
    git clone https://github.com/whispers/whispers.git $HOME/whispers && pip install -r $HOME/whispers/requirements.txt
    git clone https://github.com/eth0izzle/shhgit.git $HOME/shhgit && cd $HOME/shhgit && go build && cd -
    
    # Install Web Crawler & Recon Tools
    echo -e "${CYAN}[+] Installing Web Crawlers & Recon tools...${RESET}"
    go install github.com/projectdiscovery/katana/cmd/katana@latest
    go install github.com/lc/gau/v2/cmd/gau@latest
    go install github.com/hakluke/hakrawler@latest
    git clone https://github.com/devanshbatham/ParamSpider.git $HOME/ParamSpider && pip install -r $HOME/ParamSpider/requirements.txt

    echo -e "${GREEN}[✔] Instalasi Selesai Silahkan Jalankan Login.py${RESET}"
}

uninstall_tools() {
    echo -e "${RED}[!] Uninstalling all tools...${RESET}"
    rm -rf $HOME/SecretFinder $HOME/whispers $HOME/shhgit $HOME/ParamSpider
    rm -rf $HOME/go/bin/*
    if [ "$OS" == "linux" ]; then
        sudo apt remove -y curl git python3-pip jq unzip
    else
        pkg uninstall -y curl git python3-pip jq unzip
    fi
    echo -e "${GREEN}[✔] Uninstall complete!${RESET}"
}

# Menu pilihan
echo -e "${CYAN}Pilih opsi:${RESET}"
echo -e "1. Install tools"
echo -e "2. Uninstall tools"
echo -e "3. Keluar"
read -p "Pilihan (1/2/3): " choice

case $choice in
    1) install_tools ;;
    2) uninstall_tools ;;
    3) exit 0 ;;
    *) echo -e "${RED}[X] Pilihan tidak valid!${RESET}" ;;
esac
