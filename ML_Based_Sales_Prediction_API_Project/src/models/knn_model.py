import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Veriyi Yükleme
df = pd.read_csv("C:/Users/BERNA/OneDrive/Masaüstü/Turkcell/ML_Based_Sales_Prediction_API_Project/src/data/processed/sales_data1.csv")

X = df[['unit_price', 'quantity', 'discount', 'TotalOrders', 'AvgOrderValue', 'TotalQuantity', 'AvgPrice']]
y = df['total_sales']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# knn = KNeighborsClassifier(n_neighbors=3)
# KNeighborsRegressor kullanarak modelinizi kurun
knn = KNeighborsRegressor(n_neighbors=3)
knn.fit(X_train_scaled, y_train)

y_pred = knn.predict(X_test_scaled)
# print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
# Hata metriklerini kullanarak başarısını değerlendirin
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print(f'Mean Absolute Error: {mae}')
print(f'Mean Squared Error: {mse}')

