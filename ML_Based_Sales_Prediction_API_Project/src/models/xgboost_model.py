import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error


# Veriyi Yükleme
df = pd.read_csv("C:/Users/BERNA/OneDrive/Masaüstü/Turkcell/ML_Based_Sales_Prediction_API_Project/src/data/processed/sales_data1.csv")

# Kullanılacak bağımsız değişkenler (features) ve bağımlı değişken (target)
X = df[['Year', 'Month', 'Day', 'category_id', 'discount', 'TotalOrders', 'AvgOrderValue', 'TotalQuantity', 'AvgPrice']]
y = df['total_sales']

# Veriyi eğitim ve test setlerine ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost modelini oluştur ve eğit
model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42)
model.fit(X_train, y_train)

# Tahmin yap ve performansı değerlendir
y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))  # squared parametresi olmadan


print("MAE:", mean_absolute_error(y_test, y_pred))
# print("RMSE:", mean_squared_error(y_test, y_pred, squared=False))
print("RMSE:", rmse)
print(f"MSE : ", (mean_squared_error(y_test, y_pred)))

print(y_test.median())
print(df["total_sales"].median())