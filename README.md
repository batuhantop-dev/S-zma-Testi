⚡ ISU SecOps — CVE-2026-1988
Eğitim Amaçlı Zafiyet Simülasyon ve Tespit Laboratuvarı
Zero-Click RCE via Bluetooth GATT & XNU Kernel UAF
CVSS 9.8 — Kritik (Critical)

Plaintext
┌─────────────────────────────────────────────────────────────────┐
│ [Zararlı Trafik] → Malformed GATT Paketi Gönderimi (>4096 Bayt) │
│ [Zararlı Trafik] → Mach IPC Port Manipülasyonu (>1024 Port)     │
│ 🚨 ISU SecOps    → Anomali Tespit Edildi & Bağlantı Kesildi!    │
└─────────────────────────────────────────────────────────────────┘
🎯 Proje Hakkında
Bu proje, Apple işletim sistemlerindeki (iOS/macOS) kritik CVE-2026-1988 çekirdek zafiyetinin mantığını kavramak amacıyla İstinye Üniversitesi akademik gereksinimleri doğrultusunda geliştirilmiştir.

Proje, gerçek bir istismar kodu barındırmak yerine; arka planda bu zafiyetin ağdaki davranışsal izlerini (paket boyutları ve port istekleri) simüle eder ve bu izleri yakalayan canlı bir Güvenlik Operasyon Merkezi (SecOps) paneli sunar.

📋 CVE Bilgileri
Alan	Detay
CVE ID	CVE-2026-1988
Zafiyet Türü	Out-of-Bounds Write & Use-After-Free (UAF)
CVSS v3.1	9.8 / Critical
Etkilenen Sistemler	iOS 19 ve öncesi, macOS Sequoia (15.x) Öncesi
Saldırı Vektörü	Bluetooth (bluetoothd) ve XNU IPC Portları
🚀 Hızlı Kurulum ve Çalıştırma
Projeyi yerel bilgisayarınızda (localhost) ayağa kaldırmak için aşağıdaki adımları izleyebilirsiniz. Sisteminizde Python 3.8+ kurulu olmalıdır.

1. Gerekli kütüphaneleri yükleyin:

Bash
pip install -r requirements.txt
2. ISU SecOps Simülatörünü başlatın:

Bash
python src/app.py
3. Paneli görüntüleyin:
Tarayıcınızı açın ve şu adrese gidin: http://127.0.0.1:5000

📁 Proje Yapısı
Gereksiz dosya kalabalığından arındırılmış, tek merkezden yönetilen modüler mimari:

Plaintext
ISU_SecOps_CVE-2026-1988/
│
├── 📂 src/                   # 🛡️ Kaynak Kod Klasörü
│   └── app.py                # Tespit Motoru, Trafik Simülatörü ve Web Paneli
│
├── 📄 .gitignore             # Git dışlama kuralları
├── 📄 Saldiri.md             # Zafiyetin olay yeri analizi ve risk matrisi
├── 📄 readme.md              # Bu vitrin dosyası
├── 📄 requirements.txt       # Gerekli kütüphaneler (Flask, Werkzeug vb.)
└── 📄 roadmap.md             # Geliştirme fazları ve yol haritası
🛡️ Tespit Kuralları (Signatures)
ISU SecOps paneli aşağıdaki anomali eşiklerine göre çalışır:

Aşama 1 (DoS / OOB Write): Bluetooth keşif paketleri 4096 Bayt sınırını aştığında tetiklenir.

Aşama 2 (RCE / UAF): Çekirdeğe yönelik saniyelik Mach Port isteği 1024 sınırını aştığında tetiklenir ve bağlantıyı keser.

⚠️ Yasal Uyarı
🔴 Bu proje yalnızca EĞİTİM, ARAŞTIRMA ve SAVUNMA amaçlıdır.
Proje kodları gerçek bir sisteme zarar verecek herhangi bir aktif saldırı aracı (exploit) içermez. Yalnızca ağ davranışlarını matematiksel olarak taklit eden bir simülatördür. Yetkisiz ağlarda test edilmesi Türk Ceza Kanunu madde 243-245 kapsamında yasa dışıdır.
