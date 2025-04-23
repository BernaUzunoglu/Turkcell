from fastapi import FastAPI
from DBSCAN.segmentation import get_segmented_data
from DBSCAN.clustering import get_product_clusters
from DBSCAN.supplier_clustering import cluster_suppliers
from DBSCAN.country_segmentation import cluster_countries

app = FastAPI(title="Müşteri Segmentasyonu API", version="1.0")

@app.get("/segments", tags=["Segmentler"])
def get_segments():
    """
    Tüm müşteri segmentlerini getirir.
    """
    df = get_segmented_data()
    return df.to_dict(orient="records")

@app.get("/outliers", tags=["Aykırı Müşteriler"])
def get_outliers():
    """
    Aykırı (outlier) müşterileri getirir.
    """
    df = get_segmented_data()
    outliers = df[df["cluster"] == -1]
    return outliers[["customer_id", "total_orders", "total_spent", "avg_order_value"]].to_dict(orient="records")

@app.get("/product-clusters", tags=["Ürün Segmentasyonu"])
def get_product_clusters_api():
    """
    Ürünleri sipariş geçmişine göre kümeler. -1 olan ürünler: niş veya az satılan ürünlerdir.
    """
    df = get_product_clusters()
    return df.to_dict(orient="records")

@app.get("/niche-products", tags=["Niş Ürünler"])
def get_niche_products():
    """
    -1 kümesine ait ürünler: alışılmadık veya az tercih edilen ürünler.
    """
    df = get_product_clusters()
    niche_df = df[df["cluster"] == -1]
    return niche_df.to_dict(orient="records")


@app.get("/supplier-clusters", tags=["Tedarikçi Segmentasyonu"])
def supplier_clusters():
    df = cluster_suppliers()
    return df.to_dict(orient="records")

@app.get("/country-clusters", tags=["Ülke Segmentasyonu"])
def country_clusters():
    df = cluster_countries()
    return df.to_dict(orient="records")