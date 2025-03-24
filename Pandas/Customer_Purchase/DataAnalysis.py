import pandas as pd
import numpy as np
import requests
import warnings

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
warnings.simplefilter(action="ignore")

# API endpointi için url linki
base_url = "http://localhost:3000/orders"

# ######################################################
# 1. API’den Veri Çekme
# ######################################################
# API'den veriyi çekme fonksiyonu
def get_orders():
    response = requests.get(base_url)

    # JSON verisini DataFrame'e çevirme
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        return df
    else:
        print("Error fetching data:", response.status_code)
        return None

# API verisini DataFrame olarak alma
df_orders = get_orders()

# Expolatory Data Analysis (EDA - Keşifci Veri Analizi)
# Veri seti hakkında genel bilgileri görmek için aşağıdaki fonksiyonu kullanabiliriz
def check_df(dataframe, head=5):
    print("############### Shape  ###############")
    print(dataframe.shape)
    print("############### Types  ###############")
    print(dataframe.dtypes)
    print("############### Head  ###############")
    print(dataframe.head(head))
    print("############### Tail  ###############")
    print(dataframe.tail(head))
    print("############### NA  ###############")
    print(dataframe.isnull().sum())
    print("############### Quantiles  ###############")
    print(dataframe.describe([0, 0.85, 0.50, 0.95, 0.99, 1]))  # bir pandas DataFrame içindeki sayısal veriler için özet istatistikleri hesaplar
    print("############### Null Datas  ###############")
    print(dataframe.isnull().head())

print(check_df(df_orders))

# ######################################################
# 2. Veri Manipülasyonu
# API’den gelen veriyi Pandas kullanarak işleyin ve aşağıdaki işlemleri gerçekleştirin:
# ######################################################

#  1- Eksik verileri tespit edip doldurma veya kaldırma (Customer Satisfaction Score)
missing_values = df_orders[df_orders.isnull().any(axis=1)]
print(missing_values)
# Kaç tane eksik değerimiz olduğuna shape ile bakalım.
print(missing_values.shape)

# Kategorik değişkenler için Diğer adında bir kategori oluşturma ve eksik verileri Unknown olarak dolduralım
df_orders["Category"].fillna("Unknown", inplace=True)

# Sayısal değişkenleri ortalama ile doldurma
df_orders["Price"].fillna(df_orders["Price"].mean(), inplace=True)
df_orders["Customer Satisfaction Score"].fillna(df_orders["Customer Satisfaction Score"].mean(), inplace=True)

# ##################################################################################################
# Customer Satisfaction Score sütununda ki eksik verileri mantıklı bir şekilde doldurma denemesi
# ##################################################################################################

# Eksik değerleri olanları belirle
missing_mask = df_orders["Customer Satisfaction Score"].isna()  # isna() df veya serilerdeki NaN değerleri bulur

# "Quantity Purchased" ve "Customer Satisfaction Score" ilişkisini anlamak için gruplama yap çünkü bir ürün çok satılmış ise beğenilmiştir. Çok tercih ediliyor demektir.
grouped = df_orders.groupby("Quantity Purchased")["Customer Satisfaction Score"].mean()

# Eksik değerleri doldurma map fonksiyonu ile df deki miktar alanına denk gelen grupladığımız değerler ile eşleşen verileri score değerleri ile doldurma
df_orders.loc[missing_values, "Customer Satisfaction Score"] = df_orders.loc[df_orders, "Quantity Purchased"].map(grouped)

# Eğer hala eksik değerler varsa, genel ortalama ile doldur
missing_values["Customer Satisfaction Score"].fillna(df_orders["Customer Satisfaction Score"].mean(), inplace=True)

score_by_quantity = df_orders.groupby("Quantity Purchased")["Customer Satisfaction Score"].mean().reset_index()
score_by_quantity.rename(columns={"Customer Satisfaction Score": "Avg_SatisfactionScore"}, inplace=True)
print(df_orders)
print(score_by_quantity)

# ##################################################################################################

# Boş değerlerin dolup dolmadığını kontrol edelim
print(df_orders.isnull().sum())

#  2- Tarih formatlarını uygun hale getirme - Kolon object tipide datetime çevirelim
df_orders["Purchase Date"] = pd.to_datetime(df_orders["Purchase Date"])

# II. YOL
df_orders["Purchase Date"] = df_orders["Purchase Date"].astype('datetime64')

# Avrupa formatına çevirme datetime kolonunda tarihsel bir işlem için örnek kullanım.
# df_orders["Purchase Date"] = pd.to_datetime(df_orders["Purchase Date"]).dt.strftime("%d/%m/%Y")

print(check_df(df_orders))

# 3- Belirli kategorilerde fiyat güncelleme
# Kategori bazlı ZAM
categories = df_orders["Category"].unique()
print(categories)
print(df_orders.head(15))

# Kategorisi Electroics olan satırlarda price değerine %30 zam yapalım
# df_orders.loc[df_orders['Category'] == 'Electronics', 'Price']
df_orders.loc[df_orders['Category'] == 'Electronics', 'Price'] *= 1.30
print(df_orders.head(15))

#  4- Müşteri memnuniyeti puanlarını analiz ederek en popüler ürünleri belirleme
popular_products = df_orders[df_orders["Customer Satisfaction Score"] >= 0]

# Her ürün için ortalama müşteri memnuniyeti puanını hesapla
average_scores = popular_products.groupby("Product Name")["Customer Satisfaction Score"].mean()

# Ortalamalarla birlikte ürünleri yazdır
popular_products_unique = average_scores.reset_index()

# Ortalamaları büyükten küçüğe sırala
popular_products_sorted = popular_products_unique.sort_values(by="Customer Satisfaction Score", ascending=False)

# İlk 5 popüler ürünü ve ortalama puanlarını yazdır
print(popular_products_sorted)
print(popular_products_sorted.head())

# ######################################################
# 3. Veri Analizi
# ######################################################
# 1 En çok satın alınan ürünleri belirleyin
most_purchased_products = df_orders.groupby("Product Name")["Quantity Purchased"].sum()
print(most_purchased_products.sort_values(ascending=False).head())

# 2- Fiyat ve satış miktarı arasındaki korelasyonu inceleyin
correlation = df_orders["Price"].corr(df_orders["Quantity Purchased"])
if correlation > 0.5:
    print("Positive correlation")
elif correlation < -0.5:
    print("Negative correlation")
else:
    print("No correlation")
print("Correlation", correlation)

# NOT : Mesela gerçek hayatta bir ürün çok satılmış ise puan değeri yüksektir. Bu şekilde iki değişken arasındaki korelasyon incelenirse +1 pozitif bir korelasyon olacaktır.

# 3- Kategorilere göre ortalama fiyat hesaplayın
average_price_by_category = df_orders.groupby("Category")["Price"].mean()
print("Ortalama fiyat",average_price_by_category)

# 4- Belirli bir zaman diliminde en çok satılan ürünleri bulun

# df_orders["Purchase Date"] = pd.to_datetime(df_orders["Purchase Date"])
df_orders["Month"] = df_orders["Purchase Date"].dt.month
df_orders["Year"] = df_orders["Purchase Date"].dt.year
most_sold_products = df_orders.groupby(["Year", "Month", "Product Name"])["Quantity Purchased"].sum()
print(most_sold_products.sort_values(ascending=False).head(18))

# 5- Müşteri harcama seviyelerine göre gruplama yapın
spending_levels = pd.qcut(df_orders["Price"], q=5, labels=["Very Low", "Low", "Medium", "High", "Very High"])
df_orders["Spending Level"] = spending_levels
print(df_orders.head(10))


# ######################################################
# 4. Dinamik Fiyatlandırma
# ######################################################

# 1- Ürünlerin ortalama fiyatlarını hesaplayarak aşırı pahalı veya ucuz ürünleri belirleyin
# 2- Piyasadan belirli bir oranda düşük fiyatlı ürünlerin fiyatını güncelleyin

# ------------ Pandas ile yapılmış versiyonu ---------------------
average_price = df_orders["Price"].mean()
print("Ortalama fiyat", average_price)

# Fiyat kategorisini belirleme
df_orders["Price Category"] = df_orders["Price"].apply(
    lambda x: "Cheap" if x < average_price * 0.7 else ("Expensive" if x > average_price * 1.3 else "Normal")
)

# Yeni fiyat sütunu (Güncellenmiş fiyat)
df_orders["Updated Price"] = df_orders.apply(
    lambda row: row["Price"] * 1.10 if row["Price Category"] == "Cheap" else row["Price"], axis=1
)

# Sonucu yazdır
print(df_orders)

#  -----------Numpy ile yapılmış versiyonu --------------------------


# Ortalama fiyatı hesapla
average_price = np.mean(df_orders["Price"].values)
print("Ortalama fiyat", average_price)

# Fiyat kategorisini belirleme
price_category = np.where(df_orders["Price"].values < average_price * 0.7, "Cheap",
                          np.where(df_orders["Price"].values > average_price * 1.3, "Expensive", "Normal"))

# Fiyat kategorisini yeni sütun olarak ekleyelim
df_orders["Price Category"] = price_category

# Yeni fiyat sütunu (Güncellenmiş fiyat) hesaplama
updated_price = np.where(df_orders["Price Category"] == "Cheap",
                         df_orders["Price"].values * 1.10, df_orders["Price"].values)

# Güncellenmiş fiyatı yeni sütun olarak ekleyelim
df_orders["Updated Price"] = updated_price

# Sonucu yazdır
print(df_orders)

# ######################################################
# 5. Ürün Öneri Sis
# ######################################################

# 1- Müşterilere, satın aldıkları ürünlere benzer en popüler ürünleri önerin
# Öneri sistemini kategori bazında geliştirin


# Müşteri bazında kategori analizini yapalım
customer_category = df_orders.groupby(["Customer ID", "Category"])["Product Name"].count().reset_index()

# Kategorileri müşteri bazında sıralayalım
customer_category["Category_Rank"] = customer_category.groupby("Customer ID")["Product Name"].rank(method="first", ascending=False)
customer_category.head(15)
# Müşterinin en çok sipariş verdiği kategoriye odaklanalım
customer_category = customer_category[customer_category["Category_Rank"] == 1].reset_index(drop=True)

# Popüler ürünleri sıralayarak alalım
popular_products_sorted = df_orders.groupby(["Category", "Product Name"])["Customer ID"].count().reset_index()
popular_products_sorted = popular_products_sorted.sort_values(by=["Category", "Customer ID"], ascending=[True, False])

# Öneri fonksiyonunu kullanarak güvenli şekilde öneri yapalım
def get_recommended_product(category):
    filtered = popular_products_sorted[popular_products_sorted["Category"] == category]
    if not filtered.empty:
        return filtered["Product Name"].values[0]
    return "No Recommendation"

customer_category["Recommended Product"] = customer_category["Category"].apply(get_recommended_product)

print(customer_category.head(100))
