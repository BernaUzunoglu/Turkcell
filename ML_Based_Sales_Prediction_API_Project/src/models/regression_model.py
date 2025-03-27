import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error


pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
# C:\Users\BERNA\OneDrive\Masaüstü\Turkcell\ML_Based_Sales_Prediction_API_Project\src\data\processed\sales_data.csv

df1 = pd.read_csv("C:/Users/BERNA/OneDrive/Masaüstü/Turkcell/ML_Based_Sales_Prediction_API_Project/src/data/processed/sales_data.csv")
df = pd.read_csv("C:/Users/BERNA/OneDrive/Masaüstü/Turkcell/ML_Based_Sales_Prediction_API_Project/src/data/processed/features.csv")
# print(df.head(10))

# CSV dosyasını oku
# df = pd.read_csv("src/data/processed/sales_data.csv")

# Gerekli sütunları seç
features = ["year", "month", "day", "order_unit_price", "quantity", "discount", "product_unit_price"]
target = "total_sales"

# print(df["total_sales"].median())

# Eksik değerleri kontrol et
df = df.dropna()

# Kategorik değişkenleri one-hot encoding yap
df = pd.get_dummies(df, columns=["category_id"], drop_first=True)

X = df.drop(['customer_id', 'OrderTotal'], axis=1)
y = df['OrderTotal']
# Özellikler ve hedef değişkeni ayır
# X = df[features]
# y = df[target]

# Veriyi eğitim ve test setlerine ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Veriyi ölçeklendir
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Lineer regresyon modelini tanımla
model = LinearRegression()

# Modeli eğit
model.fit(X_train_scaled, y_train)

# Test seti üzerinde tahmin yap
y_pred = model.predict(X_test_scaled)


# Hata metrikleri - hata performansını değerlendir
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"MAE: {mae:.2f}")
print(f"MSE: {mse:.2f}")
print(f"RMSE: {rmse:.2f}")
print(df["OrderTotal"].median())
