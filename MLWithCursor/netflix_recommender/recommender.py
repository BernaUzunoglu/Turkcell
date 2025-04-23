# -*- coding: utf-8 -*-
import numpy as np
from sklearn.cluster import KMeans
from sqlalchemy.orm import Session
from models import Film, Kullanici, Puan, Izleme, Kategori
import pandas as pd

class FilmOneriSistemi:
    def __init__(self, n_clusters=5):
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.film_ozellikleri = None
        self.film_kumeleri = None
        
    def film_ozelliklerini_olustur(self, db: Session):
        # Filmlerin özelliklerini veritabanından al
        filmler = db.query(Film).all()
        
        # Her film için özellik vektörü oluştur
        ozellikler = []
        for film in filmler:
            # Film özellikleri
            film_ozellik = [
                film.yil,
                film.sure,
                film.imdb_puani,
                # Kategori bilgileri (one-hot encoding)
                *[1 if k in [k.ad for k in film.kategoriler] else 0 for k in db.query(Kategori).all()]
            ]
            ozellikler.append(film_ozellik)
        
        self.film_ozellikleri = np.array(ozellikler)
        
    def kumeleri_olustur(self):
        if self.film_ozellikleri is None:
            raise ValueError("Önce film özelliklerini oluşturun")
        
        # K-means ile kümeleri oluştur
        self.kmeans.fit(self.film_ozellikleri)
        self.film_kumeleri = self.kmeans.labels_
        
    def kullanici_tercihlerini_analiz_et(self, db: Session, kullanici_id: int):
        # Kullanıcının izlediği filmleri ve puanlarını al
        izlemeler = db.query(Izleme).filter(Izleme.kullanici_id == kullanici_id).all()
        puanlar = db.query(Puan).filter(Puan.kullanici_id == kullanici_id).all()
        
        # Kullanıcının tercih ettiği kümeleri bul
        tercih_edilen_kumeler = []
        for izleme in izlemeler:
            film_id = izleme.film_id
            film_index = next(i for i, f in enumerate(db.query(Film).all()) if f.id == film_id)
            tercih_edilen_kumeler.append(self.film_kumeleri[film_index])
        
        # En çok tercih edilen kümeyi bul
        if tercih_edilen_kumeler:
            en_cok_tercih = max(set(tercih_edilen_kumeler), key=tercih_edilen_kumeler.count)
            return en_cok_tercih
        return None
        
    def oneri_yap(self, db: Session, kullanici_id: int, n_oneri=5):
        if self.film_kumeleri is None:
            raise ValueError("Önce kümeleri oluşturun")
        
        # Kullanıcının tercih ettiği kümeyi bul
        tercih_edilen_kume = self.kullanici_tercihlerini_analiz_et(db, kullanici_id)
        
        if tercih_edilen_kume is None:
            # Kullanıcının tercihi yoksa, en popüler filmleri öner
            return db.query(Film).order_by(Film.imdb_puani.desc()).limit(n_oneri).all()
        
        # Aynı kümedeki filmleri bul
        ayni_kumedeki_filmler = []
        for i, film in enumerate(db.query(Film).all()):
            if self.film_kumeleri[i] == tercih_edilen_kume:
                ayni_kumedeki_filmler.append(film)
        
        # Kullanıcının izlediği filmleri çıkar
        izlenen_filmler = [izleme.film_id for izleme in db.query(Izleme).filter(Izleme.kullanici_id == kullanici_id).all()]
        onerilecek_filmler = [f for f in ayni_kumedeki_filmler if f.id not in izlenen_filmler]
        
        # IMDB puanına göre sırala ve en iyi n_oneri filmi seç
        onerilecek_filmler.sort(key=lambda x: x.imdb_puani, reverse=True)
        return onerilecek_filmler[:n_oneri] 