# 0Zer0APIScanner

![GitHub Repo](https://img.shields.io/badge/GitHub-0Zer0APIScanner-blue?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-green?style=flat-square)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-orange?style=flat-square)

## 🛠 Everything Can Be Hacked 🔥

**0Zer0APIScanner** adalah tools otomatis untuk melakukan reconnaissance terhadap API, mencari endpoint tersembunyi, dan mendeteksi **secrets** (API keys, token, credentials) yang mungkin bocor.

---

## 🎯 **Fitur**
✅ **API Recon**: Mengumpulkan endpoint API menggunakan `gau`, `waybackurls`, dan `ParamSpider`  
✅ **JavaScript Analysis**: Menemukan API dari file `.js` menggunakan `subjs`, `katana`, dan `linkfinder`  
✅ **Secret Finder**: Mendeteksi API keys dan credentials menggunakan `trufflehog` & `gitleaks`  
✅ **Full API Scan**: Jalankan semua fitur di atas dalam satu perintah  

---

## 🚀 **Instalasi**
### 📌 **Di Linux (Ubuntu, Kali, Parrot, dll.)**
1. Clone repository:
   ```sh
   git clone https://github.com/AryzXploit/0Zer0APIScanner.git
   cd 0Zer0APIScanner
   ```
2. Install dependencies:
   ```sh
   sudo apt update && sudo apt install python3 python3-pip -y
   pip install -r requirements.txt
   ```

---

### 📌 **Di Termux (Android)**
1. Update dan install Python:
   ```sh
   pkg update && pkg upgrade
   pkg install python git -y
   ```
2. Clone repository:
   ```sh
   git clone https://github.com/AryzXploit/0Zer0APIScanner.git
   cd 0Zer0APIScanner
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

---

## 🔥 **Cara Penggunaan**
1. Jalankan tools:
   ```sh
   python ws.py
   ```
2. Pilih mode scanning yang tersedia:  
   - **1⃣ API Recon** → Mencari endpoint API  
   - **2⃣ JavaScript Analysis** → Menganalisis file `.js`  
   - **3⃣ Secret Finder** → Mendeteksi API keys & credentials  
   - **4⃣ Full API Scan** → Scan semua fitur sekaligus  

3. Masukkan **domain target**, lalu tunggu hasilnya!

---

## 🛠 **Dependencies**
- Python3
- `gau`, `waybackurls`, `katana`, `subjs`, `trufflehog`, `gitleaks`
- `pip install -r requirements.txt`

---

## 🏆 **Kontributor**
🔥 **Muhammad Arya Arjuna Habibullah** (**AryzXploit**) - Developer & Bug Hunter  
🔥 **Tim KaciwwSec** - Support & Testing  

> 🚀 *Mau kontribusi? Pull request selalu terbuka!*  

---

## 📌 **Kontak & Sosial Media**
👨‍💻 **GitHub**: [AryzXploit](https://github.com/AryzXploit)  
🌐 **Website**: [AryzXploit](https://lostsec.xyz)  
📲 **Discord Server**: DM di GitHub untuk invite  

🔥 **Everything Can Be Hacked!** 🔥

