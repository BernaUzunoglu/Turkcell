import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import numpy as np
import sklearn

# Veriyi Yükleme
df = pd.read_csv("C:/Users/BERNA/OneDrive/Masaüstü/Turkcell/ML_Based_Sales_Prediction_API_Project/src/data/processed/sales_data.csv")

# Aykırı değerleri kaldır
df = df[np.abs(df["total_sales"] - df["total_sales"].mean()) <= (3 * df["total_sales"].std())]

print("-----------------")
print(df.shape)
print("-----------------")

X = df[["quantity", "order_unit_price", "discount"]]
y = df["total_sales"]

# Veriyi ölçekleme
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Model Eğitme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

# Tahmin ve Performans
y_pred = model.predict(X_test)
print("MSE:", mean_squared_error(y_test, y_pred))



from sklearn.ensemble import RandomForestRegressor

# Random Forest Modeli
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Tahmin ve yeni MSE
y_pred_rf = rf_model.predict(X_test)
print("MSE (Random Forest):", mean_squared_error(y_test, y_pred_rf))

print(y_test.median())
