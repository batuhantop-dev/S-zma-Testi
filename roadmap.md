🔴 Faz 1 — Zafiyet Araştırması ve Kavramsal Analiz
Hedef
"Zero-Click" (Sıfır Tıklama) mimarisinin iOS üzerinde nasıl çalıştığını ve dış ağdan sistem çekirdeğine (Kernel) nasıl ulaşıldığını deşifre etmek.

Teknik Detaylar
Saldırı Vektörü: Bluetooth (GATT Protokolü)

Hedef Servis: bluetoothd (Sandbox Bypass)

Çekirdek Açığı: XNU Mach IPC Port taşması üzerinden Use-After-Free (UAF)

Başarı Kriteri
[x] Saldırının OOB Write ve UAF olarak 2 faza ayrıldığının anlaşılması.

[x] Detaylı olayın yeri incelemesinin Saldiri.md içine yazılması.

🟡 Faz 2 — Tespit Kurallarının (Ruleset) Belirlenmesi
Hedef
Saldırganın kullandığı manipüle edilmiş paketlerin, normal ağ trafiğinden nasıl ayırt edileceğine dair matematiksel sınırların çizilmesi.

Belirlenen İmzalar (Signatures)
Plaintext
Anomali 1 (OOB Write) : Gelen GATT Paketi > 4096 Bayt
Anomali 2 (Mach UAF)  : İstenen Port Sayısı > 1024
🟠 Faz 3 & 4 — Simülasyon Motoru ve Web Arayüzü
Script: website/app.py
Yapılacaklar
Veri Üreticisi: Python random ve time kütüphaneleriyle hem temiz bağlantıları hem de zararlı CVE-2026-1988 paketlerini üreten bir arka plan döngüsü yazılması.

API Endpoint: Üretilen verilerin JSON formatında dışarı aktarılması (/api/live-stream).

Frontend (Önyüz): Bootstrap 5 kullanılarak karanlık mod (Dark Mode) destekli, kurumsal "Güvenlik Operasyon Merkezi" tasarımının kodlanması.

Asenkron Akış: JavaScript fetch() API kullanılarak sayfa yenilenmeden verilerin terminal ekranına düşürülmesi.

Beklenen Çıktı
4096 Bayt ve 1024 Port sınırını aşan paketlerde ekranda 🚨 CRITICAL: CVE-2026-1988 uyarısının yanması.

🟣 Faz 5 — Dış Saldırı ve Tarama Araçları
Yapılacaklar
Zafiyetli cihazları bulmak ve sistemi test etmek için sahte (mock) betiklerin hazırlanması.

scanner.sh: Projeyi başlatan ana terminal arayüzü (CLI).


🟢 Faz 6 — Savunma & Düzeltme Önerileri (Remediation)
Yapılacaklar
Sistem yöneticileri için aksiyon planının oluşturulması.

CVSS Skorlaması: 9.8 (Kritik) matrisinin çıkarılması.

Geçici Çözüm (Mitigation): Güvenlik duvarlarında 4096B limitinin kural olarak (Drop) eklenmesi.

Kalıcı Çözüm (Patch): Apple cihazların iOS 20 ve macOS Sequoia üstüne güncellenmesinin tavsiye edilmesi (kalloc.mach_port izolasyonu).

⚠️ Yasal Uyarı
Bu proje yalnızca EĞİTİM ve SAVUNMA amaçlıdır.
Proje içeriği zararlı bir istismar (exploit) barındırmaz, savunma sistemlerinin nasıl çalışması gerektiğini gösteren bir ağ simülasyonudur. Yetkisiz sistemlere saldırı, TCK madde 243-245 kapsamında cezai yaptırıma tabidir.