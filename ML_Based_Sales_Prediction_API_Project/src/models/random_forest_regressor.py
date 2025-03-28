import pandas as pd

# Veriyi Yükleme
data = pd.read_csv("C:/Users/BERNA/OneDrive/Masaüstü/Turkcell/ML_Based_Sales_Prediction_API_Project/src/data/processed/sales_data.csv")

# Sipariş başına toplam tutarı hesapla
data['TotalProductValue'] = data['order_unit_price'] * data['quantity'] * (1 - data['discount'])
order_totals = data.groupby('order_id')['TotalProductValue'].sum().reset_index()
order_totals.columns = ['OrderID', 'OrderTotal']

# Sipariş başına özellikleri oluştur
order_features = data.drop_duplicates('OrderID')[['OrderID', 'CustomerID', 'EmployeeID', 'OrderDate',
                                                'Freight', 'ShipCity', 'ShipCountry', 'ShipVia']]

# Siparişteki ürün çeşitliliği
product_variety = data.groupby('OrderID').agg(
    ProductCount=('ProductID', 'count'),
    UniqueCategories=('CategoryID', 'nunique')
).reset_index()

# Müşteri istatistikleri (geçmiş siparişler)
customer_stats = data.groupby('CustomerID').agg(
    CustomerOrderCount=('OrderID', 'nunique'),
    CustomerAvgOrderValue=('TotalProductValue', 'mean')
).reset_index()

# Tüm özellikleri birleştir
final_data = order_features.merge(order_totals, on='OrderID') \
                          .merge(product_variety, on='OrderID') \
                          .merge(customer_stats, on='CustomerID')

# Tarih özellikleri
final_data['OrderDate'] = pd.to_datetime(final_data['OrderDate'])
final_data['OrderYear'] = final_data['OrderDate'].dt.year
final_data['OrderMonth'] = final_data['OrderDate'].dt.month
final_data['OrderDay'] = final_data['OrderDate'].dt.day
final_data['OrderDayOfWeek'] = final_data['OrderDate'].dt.dayofweek

# Kategorik değişkenleri işleme
categorical_cols = ['CustomerID', 'EmployeeID', 'ShipCity', 'ShipCountry', 'ShipVia']
label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    final_data[col] = le.fit_transform(final_data[col].astype(str))
    label_encoders[col] = le

# Son veri seti
features = ['Freight', 'ProductCount', 'UniqueCategories',
            'CustomerOrderCount', 'CustomerAvgOrderValue',
            'OrderYear', 'OrderMonth', 'OrderDay', 'OrderDayOfWeek'] + categorical_cols

X = final_data[features]
y = final_data['OrderTotal']

# Veriyi ölçeklendirme
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Eğitim ve test setlerine ayırma
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)