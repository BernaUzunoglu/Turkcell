from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from models import Base, Film, Kategori, Kullanici, Izleme, Puan

# .env dosyasını yükle
load_dotenv()

# Veritabanı bağlantı URL'sini oluştur
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Engine oluştur
engine = create_engine(DATABASE_URL)

try:
    # Tüm tabloları temizle
    print("🗑️ Veritabanı temizleniyor...")
    Base.metadata.drop_all(engine)
    
    # Tabloları yeniden oluştur
    print("🔄 Tablolar yeniden oluşturuluyor...")
    Base.metadata.create_all(engine)
    
    print("✅ Veritabanı başarıyla temizlendi ve tablolar yeniden oluşturuldu!")

except Exception as e:
    print("❌ Veritabanı temizleme işlemi başarısız!")
    print(f"Hata: {str(e)}") 