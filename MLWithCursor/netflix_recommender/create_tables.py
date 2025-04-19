from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from models import Base

# .env dosyasını yükle
load_dotenv()

# Veritabanı bağlantı bilgilerini al
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Bağlantı URL'sini oluştur
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    # Veritabanı bağlantısını oluştur
    engine = create_engine(DATABASE_URL)
    
    # Tabloları oluştur
    Base.metadata.create_all(bind=engine)
    print("✅ Tablolar başarıyla oluşturuldu!")
    print("Oluşturulan tablolar:")
    for table_name in Base.metadata.tables.keys():
        print(f"- {table_name}")
        
except Exception as e:
    print("❌ Tablo oluşturma işlemi başarısız!")
    print(f"Hata: {str(e)}") 