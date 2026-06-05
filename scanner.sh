#!/bin/bash

# ISU SecOps - Zafiyet Tarama Simülatörü Başlatıcı
echo -e "\033[1;34m[*] ISU SecOps Core-Gateway Tarayıcı Başlatılıyor...\033[0m"
echo "[+] Hedef Ağ: Localhost (Simülasyon Modu)"
echo "[+] Hedef Zafiyet: CVE-2026-1988 (iOS Zero-Click)"
sleep 1

echo "[*] Ağ arayüzü dinlemeye alınıyor..."
sleep 1
echo -e "\033[1;32m[OK] Servis aktif. Web panelini başlatmak için 'website/app.py' dosyasını çalıştırın.\033[0m"