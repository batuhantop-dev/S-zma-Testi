from flask import Flask, render_template_string, jsonify
import random
import time

app = Flask(__name__)

# 1. Arka Planda Trafik Simülasyonu
def simulasyon_trafigi_uret():
    """
    Bu fonksiyon ağ trafiğini taklit eder. %20 ihtimalle CVE-2026-1988
    zafiyetini tetiklemeye çalışan anormal sınırlar üretir.
    """
    zararlimi = random.choice([True, False, False, False, False])

    if zararlimi:
        # SALDIRI SENARYOSU: Sınırları aşan paketler (OOB Write & Kernel UAF)
        return {
            "timestamp": time.strftime("%H:%M:%S"),
            "ip": f"192.168.1.{random.randint(100, 254)}",
            "paket_boyutu": random.randint(4100, 6000), # 4096 Bayt Sınırı Aşıldı!
            "port_sayisi": random.randint(1025, 2000),  # 1024 Port Sınırı Aşıldı!
            "durum": "🚨 CRITICAL: CVE-2026-1988 (Büyük Paket & Port Limiti Aşıldı) - Saldırı Engellendi!",
            "stil": "danger" # Kırmızı Neon Alarm
        }
    else:
        # NORMAL TRAFİK SENARYOSU: Temiz bağlantılar
        return {
            "timestamp": time.strftime("%H:%M:%S"),
            "ip": f"10.0.0.{random.randint(2, 99)}",
            "paket_boyutu": random.randint(64, 1500),   # Normal Bluetooth paketi
            "port_sayisi": random.randint(1, 100),      # Normal port isteği
            "durum": "✅ Normal Traffic - Güvenli Bağlantı",
            "stil": "success" # Mavi/Yeşil Normal Akış
        }

# 2. GÖRSEL ARAYÜZ: İstinye Üniversitesi SecOps Paneli (HTML/CSS/JS)
HTML_SABLONU = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>ISU SecOps - Enterprise Gateway Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .navbar { background-color: #161b22; border-bottom: 2px solid #58a6ff; }
        .navbar-brand { color: #58a6ff !important; font-weight: bold; letter-spacing: 1px; }
        .card { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; margin-bottom: 20px; }
        .card-header { background-color: #21262d; border-bottom: 1px solid #30363d; font-weight: bold; color: #58a6ff; }
        .alarm-box { padding: 15px; margin: 10px 0; border-radius: 6px; font-family: monospace; animation: fadeIn 0.5s ease-in-out; }
        .bg-danger { background-color: rgba(248, 81, 73, 0.15) !important; border: 1px solid #f85149; color: #ff7b72; }
        .bg-success { background-color: rgba(56, 139, 253, 0.1) !important; border: 1px solid #388bfd; color: #58a6ff; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
    <script>
        // Sayfayı yenilemeden her 2.5 saniyede bir arkadaki dedektiften veri çeker
        setInterval(function() {
            fetch('/api/live-stream')
                .then(response => response.json())
                .then(data => {
                    let logContainer = document.getElementById('log-stream');
                    let yeniAlarm = document.createElement('div');
                    yeniAlarm.className = 'alarm-box bg-' + data.stil;
                    yeniAlarm.innerHTML = `<strong>[${data.timestamp}]</strong> Origin IP: ${data.ip} | Paket Boyutu: ${data.paket_boyutu}B | İstenen Port: ${data.port_sayisi} <br> >>> ${data.durum}`;
                    
                    // En yeni alarmı en üste ekle
                    logContainer.insertBefore(yeniAlarm, logContainer.firstChild);
                    
                    // Ekranda 6 satırdan fazla log birikmesin (Performans için)
                    if (logContainer.children.length > 6) {
                        logContainer.removeChild(logContainer.lastChild);
                    }
                });
        }, 2500);
    </script>
</head>
<body>

    <nav class="navbar navbar-dark shadow">
        <div class="container-fluid">
            <span class="navbar-brand mb-0 h1">🛡️ ISU SecOps | İstinye University Security Operations Center</span>
            <span class="badge bg-primary">🔒 NODE: CORE-GATEWAY-01</span>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <div class="col-md-4">
                <div class="card shadow">
                    <div class="card-header">🎯 Target Threat Architecture</div>
                    <div class="card-body">
                        <h5><strong>CVE-2026-1988</strong></h5>
                        <p class="text-muted" style="font-size: 0.9em;">iOS Zero-Click RCE & XNU Kernel UAF</p>
                        <hr style="border-color: #30363d;">
                        <h6><strong>Yakalama Kuralları (Signatures):</strong></h6>
                        <ul>
                            <li>GATT Paket Limiti: <span class="text-danger">Max 4096B</span></li>
                            <li>Mach Port Limiti: <span class="text-danger">Max 1024</span></li>
                            <li>Aksiyon: <span class="text-warning">Anında Kaynak Engelleme</span></li>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="col-md-8">
                <div class="card shadow">
                    <div class="card-header">📊 Live Incident Feed (Simulated Network Interface)</div>
                    <div class="card-body">
                        <div id="log-stream">
                            <div class="alarm-box bg-success">
                                <strong>[Sistem Aktif]</strong> Ağ arayüzü ve çekirdek log havuzu dinleniyor...
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</body>
</html>
"""

#3. FLASK ROUTE AYARLARI
@app.route('/')
def ana_sayfa():
    # Kullanıcı siteye girdiğinde arayüzü göster
    return render_template_string(HTML_SABLONU)

@app.route('/api/live-stream')
def canli_log_api():
    # JavaScript'in 2.5 saniyede bir arka plandan istediği JSON verisi
    return jsonify(simulasyon_trafigi_uret())

if __name__ == '__main__':
    print("="*50)
    print("İSÜ SecOps Simülasyonu Başlatıldı!")
    print("Çalışan paneli görmek için tarayıcınızda şu adrese gidin:")
    print("http://127.0.0.1:5000")
    print("="*50)
    app.run(debug=True, port=5000)