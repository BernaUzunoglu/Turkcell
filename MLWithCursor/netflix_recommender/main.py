# -*- coding: utf-8 -*-
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from netflix_recommender import models
from netflix_recommender.database import engine, get_db
from netflix_recommender.recommender import FilmOneriSistemi
from pydantic import BaseModel
from datetime import datetime
import os

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Film Öneri Sistemi")

# Öneri sistemi örneği
oneri_sistemi = FilmOneriSistemi()

# Pydantic modelleri
class FilmBase(BaseModel):
    baslik: str
    aciklama: str
    yil: int
    sure: int
    imdb_puani: float

class FilmCreate(FilmBase):
    kategori_ids: List[int]

class Film(FilmBase):
    id: int
    kategoriler: List[str]

    class Config:
        from_attributes = True

class KullaniciBase(BaseModel):
    kullanici_adi: str
    email: str

class KullaniciCreate(KullaniciBase):
    sifre: str

class Kullanici(KullaniciBase):
    id: int
    olusturma_tarihi: datetime

    class Config:
        from_attributes = True

class PuanBase(BaseModel):
    film_id: int
    puan: int

class IzlemeBase(BaseModel):
    film_id: int
    izlenen_sure: int

# API endpoint'leri
@app.post("/filmler/", response_model=Film)
def film_olustur(film: FilmCreate, db: Session = Depends(get_db)):
    db_film = models.Film(
        baslik=film.baslik,
        aciklama=film.aciklama,
        yil=film.yil,
        sure=film.sure,
        imdb_puani=film.imdb_puani
    )
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    
    # Kategorileri ekle
    for kategori_id in film.kategori_ids:
        kategori = db.query(models.Kategori).filter(models.Kategori.id == kategori_id).first()
        if kategori:
            db_film.kategoriler.append(kategori)
    
    db.commit()
    return db_film

@app.post("/kullanicilar/", response_model=Kullanici)
def kullanici_olustur(kullanici: KullaniciCreate, db: Session = Depends(get_db)):
    db_kullanici = models.Kullanici(
        kullanici_adi=kullanici.kullanici_adi,
        email=kullanici.email,
        sifre_hash=kullanici.sifre  # Gerçek uygulamada şifre hash'lenmelidir
    )
    db.add(db_kullanici)
    db.commit()
    db.refresh(db_kullanici)
    return db_kullanici

@app.post("/puanlar/")
def puan_ver(puan: PuanBase, kullanici_id: int, db: Session = Depends(get_db)):
    db_puan = models.Puan(
        kullanici_id=kullanici_id,
        film_id=puan.film_id,
        puan=puan.puan
    )
    db.add(db_puan)
    db.commit()
    return {"message": "Puan başarıyla kaydedildi"}

@app.post("/izlemeler/")
def izleme_kaydet(izleme: IzlemeBase, kullanici_id: int, db: Session = Depends(get_db)):
    db_izleme = models.Izleme(
        kullanici_id=kullanici_id,
        film_id=izleme.film_id,
        izlenen_sure=izleme.izlenen_sure
    )
    db.add(db_izleme)
    db.commit()
    return {"message": "İzleme kaydı başarıyla oluşturuldu"}

@app.get("/oneriler/{kullanici_id}", response_model=List[Film])
def onerileri_getir(kullanici_id: int, n_oneri: int = 5, db: Session = Depends(get_db)):
    # Öneri sistemini güncelle
    oneri_sistemi.film_ozelliklerini_olustur(db)
    oneri_sistemi.kumeleri_olustur()
    
    # Önerileri al
    oneriler = oneri_sistemi.oneri_yap(db, kullanici_id, n_oneri)
    return oneriler

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 