from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from models import Base, Film, Kategori, Kullanici, Izleme, Puan
from datetime import datetime, timedelta
from passlib.hash import bcrypt
import random

# .env dosyasını yükle
load_dotenv()

# Veritabanı bağlantı URL'sini oluştur
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Engine ve Session oluştur
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    # Kategoriler
    kategoriler = [
        "Aksiyon", "Komedi", "Drama", "Bilim Kurgu", "Romantik",
        "Gerilim", "Macera", "Animasyon", "Belgesel", "Suç"
    ]
    
    kategori_objeleri = {}
    for kategori_adi in kategoriler:
        # Kategori zaten var mı kontrol et
        existing_kategori = db.query(Kategori).filter(Kategori.ad == kategori_adi).first()
        if existing_kategori:
            kategori_objeleri[kategori_adi] = existing_kategori
            print(f"ℹ️ Kategori '{kategori_adi}' zaten mevcut")
        else:
            kategori = Kategori(ad=kategori_adi)
            db.add(kategori)
            kategori_objeleri[kategori_adi] = kategori
            print(f"✅ Kategori '{kategori_adi}' eklendi")
    
    db.commit()
    print("\n✅ Kategori işlemleri tamamlandı")

    # Filmler
    filmler = [
        {
            "baslik": "Başlangıç",
            "aciklama": "Rüyalara girip bilinçaltından bilgi çalan bir hırsız.",
            "yil": 2010,
            "sure": 148,
            "imdb_puani": 8.8,
            "kategoriler": ["Aksiyon", "Bilim Kurgu", "Gerilim"]
        },
        {
            "baslik": "Esaretin Bedeli",
            "aciklama": "Hayatını hapishanede geçiren bir bankacının hikayesi.",
            "yil": 1994,
            "sure": 142,
            "imdb_puani": 9.3,
            "kategoriler": ["Drama", "Suç"]
        },
        {
            "baslik": "Baba",
            "aciklama": "Bir mafya ailesinin hikayesi.",
            "yil": 1972,
            "sure": 175,
            "imdb_puani": 9.2,
            "kategoriler": ["Drama", "Suç"]
        },
        {
            "baslik": "Kara Şövalye",
            "aciklama": "Batman'in Joker ile mücadelesi.",
            "yil": 2008,
            "sure": 152,
            "imdb_puani": 9.0,
            "kategoriler": ["Aksiyon", "Suç", "Drama"]
        },
        {
            "baslik": "Matrix",
            "aciklama": "Simülasyon dünyasında geçen bir kurtuluş hikayesi.",
            "yil": 1999,
            "sure": 136,
            "imdb_puani": 8.7,
            "kategoriler": ["Aksiyon", "Bilim Kurgu"]
        },
        {
            "baslik": "Forrest Gump",
            "aciklama": "Saf bir adamın olağanüstü yaşam hikayesi.",
            "yil": 1994,
            "sure": 142,
            "imdb_puani": 8.8,
            "kategoriler": ["Drama", "Romantik"]
        },
        {
            "baslik": "Yüzüklerin Efendisi",
            "aciklama": "Bir yüzüğü yok etmek için çıkılan destansı yolculuk.",
            "yil": 2001,
            "sure": 178,
            "imdb_puani": 8.9,
            "kategoriler": ["Macera", "Drama", "Aksiyon"]
        },
        {
            "baslik": "Toy Story",
            "aciklama": "Oyuncakların gizli yaşamı.",
            "yil": 1995,
            "sure": 81,
            "imdb_puani": 8.3,
            "kategoriler": ["Animasyon", "Macera", "Komedi"]
        },
        {
            "baslik": "Gezegenimiz",
            "aciklama": "Dünya'nın muhteşem doğal yaşamı.",
            "yil": 2006,
            "sure": 96,
            "imdb_puani": 8.4,
            "kategoriler": ["Belgesel"]
        },
        {
            "baslik": "Zindan Adası",
            "aciklama": "Bir akıl hastanesinde geçen gizemli hikaye.",
            "yil": 2010,
            "sure": 138,
            "imdb_puani": 8.2,
            "kategoriler": ["Gerilim", "Drama"]
        }
    ]

    film_objeleri = []
    for film_data in filmler:
        # Film zaten var mı kontrol et
        existing_film = db.query(Film).filter(Film.baslik == film_data["baslik"]).first()
        if existing_film:
            film_objeleri.append(existing_film)
            print(f"ℹ️ Film '{film_data['baslik']}' zaten mevcut")
        else:
            film = Film(
                baslik=film_data["baslik"],
                aciklama=film_data["aciklama"],
                yil=film_data["yil"],
                sure=film_data["sure"],
                imdb_puani=film_data["imdb_puani"]
            )
            for kategori_adi in film_data["kategoriler"]:
                film.kategoriler.append(kategori_objeleri[kategori_adi])
            db.add(film)
            film_objeleri.append(film)
            print(f"✅ Film '{film_data['baslik']}' eklendi")
    
    db.commit()
    print("\n✅ Film işlemleri tamamlandı")

    # Kullanıcılar
    kullanicilar = [
        {"kullanici_adi": "ahmet123", "email": "ahmet@email.com", "sifre": "sifre123"},
        {"kullanici_adi": "ayse456", "email": "ayse@email.com", "sifre": "sifre456"},
        {"kullanici_adi": "mehmet789", "email": "mehmet@email.com", "sifre": "sifre789"},
        {"kullanici_adi": "zeynep321", "email": "zeynep@email.com", "sifre": "sifre321"},
        {"kullanici_adi": "can654", "email": "can@email.com", "sifre": "sifre654"}
    ]

    kullanici_objeleri = []
    for kullanici_data in kullanicilar:
        # Kullanıcı zaten var mı kontrol et
        existing_kullanici = db.query(Kullanici).filter(
            (Kullanici.kullanici_adi == kullanici_data["kullanici_adi"]) |
            (Kullanici.email == kullanici_data["email"])
        ).first()
        
        if existing_kullanici:
            kullanici_objeleri.append(existing_kullanici)
            print(f"ℹ️ Kullanıcı '{kullanici_data['kullanici_adi']}' zaten mevcut")
        else:
            kullanici = Kullanici(
                kullanici_adi=kullanici_data["kullanici_adi"],
                email=kullanici_data["email"],
                sifre_hash=bcrypt.hash(kullanici_data["sifre"])
            )
            db.add(kullanici)
            kullanici_objeleri.append(kullanici)
            print(f"✅ Kullanıcı '{kullanici_data['kullanici_adi']}' eklendi")
    
    db.commit()
    print("\n✅ Kullanıcı işlemleri tamamlandı")

    # İzleme kayıtları ve puanlar
    for kullanici in kullanici_objeleri:
        # Her kullanıcı için rastgele 3-7 film seç
        izlenecek_filmler = random.sample(film_objeleri, random.randint(3, 7))
        
        for film in izlenecek_filmler:
            # İzleme kaydı zaten var mı kontrol et
            existing_izleme = db.query(Izleme).filter(
                Izleme.kullanici_id == kullanici.id,
                Izleme.film_id == film.id
            ).first()
            
            if not existing_izleme:
                # İzleme kaydı ekle
                izleme = Izleme(
                    kullanici_id=kullanici.id,
                    film_id=film.id,
                    izleme_tarihi=datetime.now() - timedelta(days=random.randint(1, 30)),
                    izlenen_sure=random.randint(film.sure - 30, film.sure)  # Filmin çoğunu izlemiş olsun
                )
                db.add(izleme)
                print(f"✅ İzleme kaydı eklendi: {kullanici.kullanici_adi} -> {film.baslik}")
            
            # Puan zaten var mı kontrol et
            existing_puan = db.query(Puan).filter(
                Puan.kullanici_id == kullanici.id,
                Puan.film_id == film.id
            ).first()
            
            if not existing_puan:
                # Puan ekle (1-5 arası)
                puan = Puan(
                    kullanici_id=kullanici.id,
                    film_id=film.id,
                    puan=random.randint(3, 5),  # Çoğunlukla olumlu puanlar
                    puan_tarihi=datetime.now() - timedelta(days=random.randint(1, 30))
                )
                db.add(puan)
                print(f"✅ Puan eklendi: {kullanici.kullanici_adi} -> {film.baslik}")
    
    db.commit()
    print("\n✅ İzleme kayıtları ve puan işlemleri tamamlandı")

    print("\n📊 Özet:")
    print(f"- {len(kategoriler)} kategori")
    print(f"- {len(filmler)} film")
    print(f"- {len(kullanicilar)} kullanıcı")
    print(f"- Rastgele izleme kayıtları ve puanlar")

except Exception as e:
    print("❌ Veri ekleme işlemi başarısız!")
    print(f"Hata: {str(e)}")
    db.rollback()

finally:
    db.close() 