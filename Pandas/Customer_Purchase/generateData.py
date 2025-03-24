import json
import random
from datetime import datetime, timedelta

# Rastgele veri oluşturmak için yardımcı listeler
urunler = ["Telefon", "Laptop", "Kulaklık", "Mouse", "Klavye", "Monitor", "Tablet", "Akıllı Saat"]
kategoriler = ["Elektronik", "Bilgisayar", "Aksesuar", "Giyilebilir Teknoloji"]

# Veri kümesi oluşturma
veri = []
for i in range(2000):
    musteri_id = random.randint(1000, 9999)
    urun_adi = random.choice(urunler)
    kategori = random.choice(kategoriler)
    fiyat = round(random.uniform(50, 5000), 2)
    satin_alma_tarihi = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
    miktar = random.randint(1, 5)
    memnuniyet_skoru = random.choice([random.randint(1, 5), None, None])  # Eksik veri ihtimali
    
    # Bazı alanları eksik bırak
    if random.random() < 0.05:
        urun_adi = None
    if random.random() < 0.05:
        kategori = None
    if random.random() < 0.03:
        fiyat = None
    
    veri.append({
        "MusteriID": musteri_id,
        "UrunAdi": urun_adi,
        "Kategori": kategori,
        "Fiyat": fiyat,
        "SatinAlmaTarihi": satin_alma_tarihi,
        "Miktar": miktar,
        "MemnuniyetSkoru": memnuniyet_skoru
    })

# JSON dosyasına kaydetme
with open("veri.json", "w", encoding="utf-8") as f:
    json.dump(veri, f, ensure_ascii=False, indent=4)

print("JSON dosyası oluşturuldu: veri.json")
