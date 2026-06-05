# 🕵️‍♂️ Zafiyet Analizi: iOS "Kapalı Bahçe"sini Aşmak ve Tespit Etmek

> **Proje Felsefesi:** Bir sızma kavramını anlamak, sadece kod yazmak değil; o kodu ağda bir polis dedektifi gibi yakalayabilmektir. "Önce anla, sonra tespit et."

Bu döküman, **CVE-2026-1988** (iOS Zero-Click RCE & XNU Kernel UAF) zafiyetini karmaşık C kodlarından arındırarak, küçük, mantıksal ve tespit edilebilir parçalara bölmektedir. 

---

## 📍 1. Nerede Durman Lazım? (Gözlem Noktası)

Bir siber dedektif olarak doğru yerde beklemezsek, suçluyu kaçırırız. iOS ekosistemine dışarıdan sızmak isteyen bir saldırganın geçmek zorunda olduğu iki güvenlik kapısı (olay yeri) vardır:

1. **Dış Sınır (Ağ Kartı Seviyesi):** Cihazın dış dünyayla konuştuğu Bluetooth GATT (Generic Attribute Profile) protokolü. 
2. **İç Kasa (Çekirdek Seviyesi):** iOS işletim sisteminin kalbi olan **XNU Kernel** ve uygulamaların birbiriyle konuştuğu **Mach Mesajlaşma (IPC)** santrali.

*👉 Bizim "İSÜ SecOps" tespit simülatörümüz tam olarak bu iki kapının arasına kurulmuş bir güvenlik kamerasıdır.*

---

## 🔍 2. Neleri Deşifre Etmen Lazım? (Ham Veriyi Çevirmek)

Ağdan gelen sıradan baytları (raw data) doğrudan okuyamayız. Saldırıyı anlamak için bu veriyi aşağıdaki filtrelere göre tercüme etmeliyiz:

* **Paket Boyutu (Buffer Size):** Gelen Bluetooth paketinin hacmi ne kadar? (Normal mi, yoksa hafızayı taşırmak için şişirilmiş mi?)
* **Kapı İstekleri (Port Descriptors):** Sistem çekirdeğine giden mesajda kaç tane "port" açılması isteniyor?

---

## 🚨 3. Çevirince Neyi İnceleyeceksin? (Suçluyu Yakalama Kuralları)

Saldırganın izlediği iki adımlı stratejiyi, sistemdeki anormallik kurallarımızla (imzalarla) şu şekilde tespit ediyoruz:

### 💥 Adım A: "Kapıyı Kırmak" (OOB Write Tespiti)
Saldırgan, cihazın Bluetooth servisine (`bluetoothd`) yapısı bilerek bozulmuş (malformed) bir paket gönderir.

* **🔎 Dedektif Kuralı:** Normal bir keşif paketi küçüktür. Eğer gelen paket **`4096 Bayt`** sınırını aşıyorsa (yeni bellek yöneticisi limitleri), bu açıkça bir **Sınır Taşması (Out-of-Bounds Write)** girişimidir. Bu bir saldırı desenidir!

### 💥 Adım B: "İçeride Yetki Almak" (Kernel UAF Tespiti)
Dış kapıyı geçen saldırgan, sistemin çökmesini sağlamak için çekirdeğe aynı anda yüzlerce sahte mesaj yollar.

* **🔎 Dedektif Kuralı:** Normal uygulamalar 3-5 port ile haberleşir. Eğer mesaj içinde **`1024'ten fazla`** Mach port isteği geliyorsa, saldırgan sistemi çift temizleme (`Double-Decrement`) hatasına zorlayarak bellekte boşluk (**Use-After-Free**) yaratmaya çalışıyordur.

> *[İpucu: Hocam, İSÜ SecOps arayüzünün (panel_goruntusu.png) bu anormallikleri yakaladığı görseli tam buraya sürükleyip bırakabilirsin.]*

---

## 📋 4. Olay Yeri Özeti (Polis Mantığı Tablosu)

Karmaşık görünen bu zafiyet zincirinin dedektif mantığıyla tek bakışta özeti:

| Olay Aşaması | Saldırganın Amacı | Kullanılan Zafiyet | Bizim Tespit Kuralımız (İmza) | Uygulanan Aksiyon |
| :--- | :--- | :--- | :--- | :--- |
| **Aşama 1** | Bluetooth Sandbox'a Girmek | `OOB Write` | Paket > **4096 Bayt** | Şüpheli Log Kaydı |
| **Aşama 2** | Çekirdek (Kernel) Yetkisi Almak | `UAF (Mach Port)` | Port Sayısı > **1024** | 🚨 **CRITICAL ALARM** |
| **Aşama 3** | Sistemi Ele Geçirmek (RCE) | `ROP Chain` | *Aşama 2'de Sistem Kapatıldı* | 🔒 **Bağlantı Engellendi** |


## Siber Güvenlik Arayüzü

<img width="1301" height="794" alt="Ekran Resmi 2026-06-05 18 23 09" src="https://github.com/user-attachments/assets/039ec70a-6a88-481f-a0f5-9b4640bee4d4" />


:

 1. Mavi Kutular (Normal ve Temiz Trafik)
Zaman Çizelgesi: 15:22:57, 15:22:54 ve 15:22:52 saatlerinde sisteme giriş yapmaya çalışan veriler.

Ne Oluyor?: Ağ üzerinden sıradan cihazlar (örneğin bir Bluetooth kulaklık veya normal bir uygulama) sisteme veri gönderiyor.

Dedektifin Analizi: Sistem bu paketleri inceliyor. Paket boyutlarına bakıyor (1444B, 1357B, 693B) ve bizim koyduğumuz 4096 Bayt sınırının çok altında olduklarını görüyor. İstedikleri port sayılarına bakıyor (13, 87, 84) ve bunların da 1024 Kernel sınırını aşmadığını teyit ediyor.

Sonuç: Kurallara uydukları için sistem onlara yeşil ışık yakıyor ve Normal Traffic - Güvenli Bağlantı damgasını vurarak geçmelerine izin veriyor.

2. Kırmızı Kutular (Suçüstü Yakalanan Saldırılar)
Zaman Çizelgesi: 15:22:50 ve 15:22:47 saatlerinde 192.168.1.161 ve 192.168.1.166 IP adreslerinden gelen şüpheli paketler.

Ne Oluyor?: Bir saldırgan, telefonun hafızasını taşırmak ve işletim sistemini çökertip yönetimi ele geçirmek için manipüle edilmiş (bozuk) devasa paketler yolluyor.

Dedektifin Analizi (Suçüstü): Dedektifimiz paketleri yakalıyor ve hemen boyutlarına bakıyor: 5814B ve 4608B. İkisi de bizim kırmızı çizgimiz olan 4096 Bayt'ı (OOB Write/Taşma sınırı) delip geçmiş! Ayrıca istedikleri port sayılarına bakıyor: 1986 ve 1348. Bunlar da 1024 sınırını (Double-Decrement hatasını tetikleyecek sınır) fazlasıyla aşmış.

Sonuç: Sistem bu çifte kural ihlalini gördüğü an bunun masum bir bağlantı değil, telefonu hacklemeye çalışan bir CVE-2026-1988 Zero-Click Saldırısı olduğunu anlıyor. Anında CRITICAL alarmını yakıp, saldırganı içeriye almadan engelliyor.x
