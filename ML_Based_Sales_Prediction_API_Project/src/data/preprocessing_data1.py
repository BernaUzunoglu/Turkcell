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
       SELECT 
        o.order_id,
        o.order_date,
        c.customer_id,
        p.product_id,
        p.product_name,
        p.category_id,
        od.unit_price,
        od.quantity,
        od.discount,
        (od.unit_price * od.quantity * (1 - od.discount)) AS total_sales
        FROM orders o
        JOIN order_details od ON o.order_id = od.order_id
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN products p ON od.product_id = p.product_id
        """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df


# Kullanım
df = load_merged_data()
print(df.head(10))

print(df.isnull().sum())

df["order_date"] = pd.to_datetime(df["order_date"])
df["Year"] = df["order_date"].dt.year
df["Month"] = df["order_date"].dt.month
df["Day"] = df["order_date"].dt.day

# Müşteri bazında toplam sipariş sayısı ve ortalama sipariş tutarı
customer_features = df.groupby("customer_id").agg(
    TotalOrders=("order_id", "nunique"),
    AvgOrderValue=("total_sales", "mean")
).reset_index()

# Ürün bazında toplam satış miktarı ve ortalama fiyat
product_features = df.groupby("product_id").agg(
    TotalQuantity=("quantity", "sum"),
    AvgPrice=("unit_price", "mean")
).reset_index()

# Veriyi birleştir
df = df.merge(customer_features, on="customer_id", how="left")
df = df.merge(product_features, on="product_id", how="left")

print(df.head(10))

df.to_csv("C:/Users/BERNA/OneDrive/Masaüstü/Turkcell/ML_Based_Sales_Prediction_API_Project/src/data/processed/sales_data1.csv", index=False)


