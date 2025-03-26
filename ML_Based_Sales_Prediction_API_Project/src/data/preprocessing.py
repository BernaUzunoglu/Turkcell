import pandas as pd
from sqlalchemy import text
from database import engine  # engine'i direkt import ediyoruz
import warnings

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
warnings.simplefilter(action="ignore")

def load_merged_data():
    """Orders, Order_Details ve Products tablolarını birleştir"""
    query = """
    SELECT o.order_id,o.order_date, od.unit_price as order_unit_price, od.quantity, od.discount,
           p.product_id,p.product_name, p.category_id, c.category_name, p.unit_price as product_unit_price
    FROM orders o
    JOIN order_details od ON o.order_id = od.order_id
    JOIN products p ON od.product_id = p.product_id
    JOIN categories c ON c.category_id = p.category_id
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df

# Kullanım
merged_df = load_merged_data()

print(merged_df)

# Ürün bazlı satış özet verisinin hazırlanması
merged_df["total_sales"] = merged_df["order_unit_price"] * merged_df["quantity"] * (1 - merged_df["discount"])


product_sales = merged_df.groupby("product_name").agg(
     total_quantity=("quantity", "sum"),
     total_revenue=("total_sales", "sum")
 ).reset_index()

# Özellik Mühendisliği:
# Ay bilgisi, ürün fiyatı, müşteri segmentasyonu gibi özellikler üretme

merged_df["order_date"] = pd.to_datetime(merged_df["order_date"])  # Tarih formatına çevir
# Yıl, Ay ve Gün sütunlarını oluştur
merged_df["year"] = merged_df["order_date"].dt.year
merged_df["month"] = merged_df["order_date"].dt.month
merged_df["day"] = merged_df["order_date"].dt.day


# CSV'yi kaydet
merged_df.to_csv("C:/Users/BERNA/OneDrive/Masaüstü/Turkcell/ML_Based_Sales_Prediction_API_Project/src/data/processed/sales_data.csv", index=False)

print(product_sales)
print(merged_df.head(10))



