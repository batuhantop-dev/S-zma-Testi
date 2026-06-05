⚡ ISU SecOps — CVE-2026-1988Eğitim Amaçlı Zafiyet Simülasyon ve Tespit LaboratuvarıZero-Click RCE via Bluetooth GATT & XNU Kernel UAFCVSS 9.8 — CriticalPlaintext┌─────────────────────────────────────────────────────────────────┐
│ [Uzak Saldırgan] → Malformed GATT Paketi Gönderimi (>4096 Bayt) │
│ → bluetoothd OOB Write (Sandbox Bypass)                         │
│ → Mach IPC Mesajları (>1024 Port) → Kernel UAF (XNU)            │
│ → 🚨 ISU SecOps Tarafından Tespit Edildi & Engellendi!          │
└─────────────────────────────────────────────────────────────────┘
⚠️ YASAL UYARI / DISCLAIMER🔴 Bu proje yalnızca EĞİTİM, ARAŞTIRMA ve SAVUNMA amaçlıdır.Buradaki kodlar gerçek sistemlere yönelik bir saldırı (payload) içermez, saldırı trafiğini simüle eder.Yetkisiz sistemlere yönelik ağ taramaları ve zafiyet istismarı Türk Ceza Kanunu madde 243-245 kapsamında suçtur.İstinye Üniversitesi (İSÜ) Sızma Testi final projesi kapsamında geliştirilmiştir. Tüm testler localhost üzerinde, izole ortamda yapılmalıdır.📋 CVE BilgileriAlanDetayCVE IDCVE-2026-1988CVSS v3.19.8 / Critical (AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)TürOut-of-Bounds Write & Use-After-Free (UAF)Kimlik DoğrulamaGerekmez (Pre-Auth / Zero-Click)Etkilenen SistemleriOS 19 ve öncesi, macOS Sequoia (15.x) ÖncesiYamalı SürümleriOS 20+, macOS Sequoia+ (kalloc.mach_port izolasyonu)Saldırı VektörüBluetooth (bluetoothd) ve XNU IPC Portları📁 Proje YapısıPlaintextISU_SecOps_CVE-2026-1988/
ISU_SecOps_CVE-2026-1988/
│
├── 📂 saldiri/               # 🗡️ Saldırı Simülasyon Araçları
├── 📂 scanner/               # 🔎 Ağ Tarama Araçları
├── 📂 website/               # 🛡️ ISU SecOps Web Paneli (app.py burada)
│
├── 📄 .gitignore             # Git ayarları
├── 📄 Saldiri.md             # Zafiyetin olay yeri analizi ve risk matrisi
├── 📄 readme.md              # Bu vitrin dosyası
├── 📄 requirements.txt       # Python bağımlılıkları
├── 📄 roadmap.md             # Proje geliştirme yol haritası
└── 📄 scanner.sh             # Başlatıcı script
🚀 Hızlı BaşlangıçGereksinimlerAraçSürümAmaçPython3.8+Tespit simülatörünü çalıştırmapipGüncelPaket yönetimiFlask2.0+Web paneli altyapısıSeçenek 1: Yerel Bilgisayarda Çalıştırma (Localhost)Bash# 1. Depoyu klonlayın ve klasöre girin
git clone https://github.com/KULLANICI_ADIN/ISU_SecOps_CVE-2026-1988.git
cd ISU_SecOps_CVE-2026-1988/codebase

# 2. Gerekli kütüphaneleri yükleyin
pip install -r ../requirements.txt
# Veya doğrudan: pip install flask

# 3. İSÜ SecOps Panelini başlatın
python app.py
# → Tarayıcınızda açın: http://127.0.0.1:5000
Seçenek 2: Kurulumsuz Bulut Ortamı (Google Colab)Eğer sisteminizde Python kurulu değilse, projeyi tarayıcı üzerinden anında test edebilirsiniz:Google Colab'de yeni bir not defteri açın.app.py kodunu yapıştırın.Kodun en altına from google.colab import output ve output.serve_kernel_port_as_iframe(5000, height=800) satırlarını ekleyerek çalıştırın.🛡️ Tehdit Avcılığı ve Savunma Rehberi (Remediation)Ağ yöneticileri ve SecOps ekipleri için acil durum eylem planı:1. Ağ Seviyesinde Tespit (ISU SecOps Kuralları)GATT Sınır Kontrolü: Bluetooth üzerinden gelen Service Discovery paketleri sürekli izlenmeli. 4096 Bayt sınırını aşan malformed (bozuk) paketler anında Drop (Düşür) edilmelidir.Mach Port Anomalileri: İşletim sisteminde saniyeler içinde 1024'ten fazla IPC Port (Kapı) isteği yapan işlemler Kernel Panic yaratmadan önce "Watchdog" tarafından Terminate (Sonlandır) edilmelidir.2. Kalıcı İyileştirme (Patching)Tüm Apple mobil ve masaüstü cihazları ivedilikle iOS 20 ve macOS Sequoia (veya üzeri) sürümlerine güncellenmelidir. Yeni sürümlerde kalloc_type ve izole kalloc.mach_port heap mimarisi ile bu UAF açığı donanımsal olarak (PAC) engellenmiştir.📚 ReferanslarKaynakOdak NoktasıApple Security UpdatesOrijinal XNU Yama BildirimiProject Zero BlogZero-Click İstismar AnaliziZDI (Zero Day Initiative)Bluetooth OOB Write Raporları📄 LisansBu proje İstinye Üniversitesi akademik gereksinimleri doğrultusunda hazırlanmış olup, tamamen eğitim odaklıdır.