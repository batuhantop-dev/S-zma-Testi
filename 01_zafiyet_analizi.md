Zafiyet Analizi: Bir Dedektif Gibi Düşünmek (CVE-2026-1988)
Bu döküman, siber güvenlikte "Önce anla, sonra kodla" prensibine dayanarak, karmaşık iOS Zero-Click zafiyetini küçük, anlaşılır ve tespit edilebilir parçalara bölmektedir.

Amacımız bu açığı kullanarak bir sisteme sızmak değil, bir siber polis gibi olay yerini inceleyip bu sızma girişimini ağda nasıl yakalayacağımızı kanıtlamaktır.

1. Nerede Durman Lazım? (Gözlem Noktası / Olay Yeri)
Saldırganın iPhone'a veya Apple cihazına sızmak için kullanacağı iki ana kapı vardır. Polisin nöbet tutacağı "köşeler" buralardır:

Dış Kapı (Ağ Arayüzü): Bluetooth yığınının (bluetoothd) dış dünyayla iletişim kurduğu GATT protokolü.

İç Kapı (İşletim Sistemi Çekirdeği): XNU Kernel içindeki "Mach Mesajlaşma" servisi (Uygulamaların birbiriyle konuştuğu santral).

2. Neleri Çevirmen (Analiz Etmen) Lazım? (Deşifre)
Ağdan gelen ham paketleri insan okuyabilir hale getirdiğimizde şunlara bakarız:

GATT Paket Boyutları: Dışarıdan gelen Bluetooth keşif paketlerinin (Service Discovery) byte cinsinden büyüklüğü nedir?

Port İsteği Sayıları: Çekirdeğe gönderilen bir mesajın içinde kaç tane "kapı/izin" (port descriptor) talep ediliyor?

3. Çevirince Neyi İnceleyeceksin ki Suçlu Olduğunu Anlayasın? (Tespit & Anormallik Arama)
İşte yakalama kurallarımız (İmzalarımız):

Anormallik 1 (Taşma / OOB Write Tespiti): Normal bir Bluetooth cihazı kendini tanıtırken küçük paketler yollar. Eğer gelen bir GATT paketinin boyutu 4096 Bayt'ı aşıyorsa, saldırgan sistemin hafızasını taşırmaya çalışıyordur. Bu bir saldırı desenidir!

Anormallik 2 (Çekirdek UAF Tespiti): İşletim sisteminde bir uygulamanın diğerine gönderdiği mesajda genellikle 3-5 port bulunur. Eğer bir mesajın içinde 1024'ten fazla port talebi varsa, saldırgan sistemi bilerek hataya (Double-Decrement) zorluyordur.

4. Polis Mantığıyla Özet
Olay Yeri: Bluetooth arayüzü ve Kernel Mesajlaşma Sistemi.

Delil: Gelen büyük paketler ve anormal çokluktaki port istekleri.

Tercüman / Dedektif: Python tabanlı "İSÜ SecOps" tespit simülatörümüz.

Tutuklama: Sistem bu 4096 Bayt ve 1024 Port sınırlarını aşan bir trafik gördüğünde anında kırmızı alarm üretir ve kaynağı engeller.



GÖRSELİN AÇIKLAMASI 
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

Sonuç: Sistem bu çifte kural ihlalini gördüğü an bunun masum bir bağlantı değil, telefonu hacklemeye çalışan bir CVE-2026-1988 Zero-Click Saldırısı olduğunu anlıyor. Anında CRITICAL alarmını yakıp, saldırganı içeriye almadan engelliyor.