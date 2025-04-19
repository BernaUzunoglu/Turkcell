from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Veritabanı bağlantı bilgilerini al
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

print("Veritabanı bağlantı bilgileri:")
print(f"Kullanıcı: {DB_USER}")
print(f"Host: {DB_HOST}")
print(f"Port: {DB_PORT}")
print(f"Veritabanı: {DB_NAME}")

# Bağlantı URL'sini oluştur
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(f"\nBağlantı URL'si: {DATABASE_URL}")

try:
    # Veritabanı bağlantısını oluştur
    print("\nBağlantı oluşturuluyor...")
    engine = create_engine(DATABASE_URL)
    
    # Bağlantıyı test et
    with engine.connect() as connection:
        print("Bağlantı başarılı! Test sorgusu çalıştırılıyor...")
        result = connection.execute(text("SELECT 1"))
        print("✅ Veritabanı bağlantısı başarılı!")
        print(f"Test sorgusu sonucu: {result.scalar()}")
        
except Exception as e:
    print("\n❌ Veritabanı bağlantısı başarısız!")
    print(f"Hata detayı: {str(e)}") 