from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yükle
load_dotenv()

# PostgreSQL bağlantı bilgileri
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# SQLAlchemy için bağlantı URL’si
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# PostgreSQL bağlantısı için motoru oluştur
engine = create_engine(DATABASE_URL, echo=True)

# Oturum yöneticisi oluştur
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Declarative base sınıfı
Base = declarative_base()

# Dependency olarak kullanılacak fonksiyon - Her istek için yeni bir oturum açar ve işlem bitince kapatır.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Veritabanı bağlantısını test etme
def test_connection():
    try:
        with engine.connect() as conn:
            print("✅ PostgreSQL bağlantısı başarılı!")
    except Exception as e:
        print(f"❌ PostgreSQL bağlantı hatası: {e}")

if __name__ == "__main__":
    test_connection()
