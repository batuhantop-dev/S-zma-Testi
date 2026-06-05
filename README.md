# ISU SecOps: CVE-2026-1988 Zafiyet Simülasyonu ve Tespit Paneli

İstinye Üniversitesi Sızma Testi final projesi kapsamında geliştirilmiş, **CVE-2026-1988 (iOS Zero-Click RCE & XNU Kernel UAF)** zafiyet zincirini ağ seviyesinde tespit etmeyi amaçlayan simülasyon ve analiz projesi.

> [!WARNING]
**Yasal Uyarı:** Bu proje tamamen eğitim ve savunma amaçlıdır. Gerçek sistemlere yönelik zararlı bir payload içermez; yalnızca saldırı mantığını simüle eder ve ağ üzerindeki anormalliklerin tespit mekanizmalarını araştırır.
> 

## Proje Nedir?

Bu proje, modern siber casusluk yazılımlarının iOS cihazları ele geçirmek için kullandığı "Kapalı Bahçe" (Walled Garden) mimarisini aşan karmaşık bir zafiyeti (CVE-2026-1988) inceler. Ancak bu karmaşık yapıyı hacklemek yerine, **"Bir siber güvenlik dedektifi bu saldırıyı ağda nasıl yakalar?"** sorusuna odaklanır.

Proje kapsamında, bu zafiyeti ağ üzerinde simüle eden ve anormal trafikleri anında yakalayan **İSÜ SecOps Web Paneli** geliştirilmiştir.

## Dedektif Mantığı (Nasıl Çalışır?)

Saldırının karmaşık C/C++ bellek manipülasyonları yerine, ağda bıraktığı izlere odaklanıyoruz:

- **Olay Yeri:** Ağ arayüzü ve çekirdek (Kernel) port iletişimleri.
- **Şüpheli Davranış 1 (OOB Write):** Gelen Bluetooth GATT paketinin **4096 Bayt** sınırını aşması.
- **Şüpheli Davranış 2 (Kernel UAF):** İşletim sistemine tek seferde **1024'ten fazla** Mach Port isteği gönderilmesi.
- **Aksiyon:** Sistem bu anormal sınır aşımlarını yakaladığında, "ISU SecOps" paneli üzerinden canlı güvenlik alarmları (Alert) üretir.

## Proje Yapısı (Bölüm Bölüm Yaklaşım)

Karmaşıklıktan uzak, anlaşılır klasör mimarisi:

Plaintext

```
├── README.md                 # Projenin vitrini ve özeti (Bu dosya)
├── 01_zafiyet_analizi.md     # Açığın dedektif mantığıyla adım adım incelenmesi
└── app.py                    # Simülasyonu ve İSÜ SecOps web panelini çalıştıran kod
```

## Kurulum ve Çalıştırma

Sistemi kendi bilgisayarınızda (localhost) test etmek için aşağıdaki adımları izleyebilirsiniz. Sistem **Python 3.x** gerektirir.

**1. Gerekli kütüphaneyi kurun:**

Bash

```
pip install flask
```

**2. SecOps panelini başlatın:**

Bash

```
python app.py
```

**3. Paneli görüntüleyin:**

- Tarayıcınızda `http://127.0.0.1:5000` adresine gidin ve canlı trafik simülasyonunu izleyin.

## Python Kurulumu Yoksa: Google Colab İle Çalıştırma

Eğer sisteminizde Python veya Flask kurulu değilse, projeyi hiçbir kurulum yapmadan bulut üzerinden **Google Colab** ile anında test edebilirsiniz:

1. Google Colab'i açın ve yeni bir not defteri oluşturun.
2. Depodaki `app.py` kodunun tamamını kopyalayıp hücreye yapıştırın.
3. Kodun **en üstüne** şu kütüphaneyi ekleyin:
   ```python
   from google.colab import output`

1. Kodun **en altındaki** çalıştırma bloğunu (`if __name__ == '__main__':` kısmı) silip **yerine** şunu yapıştırın:Python
    
    ```
    if __name__ == '__main__':
        output.serve_kernel_port_as_iframe(5000, height=800)
        app.run(port=5000)
    ```
    
2. Hücreyi çalıştırın (Play butonu). İSÜ SecOps Paneli yeni bir sekmeye gerek kalmadan doğrudan kod hücresinin altında açılacaktır!