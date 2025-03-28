import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, learning_curve
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

df = pd.read_csv("C:/Users/BERNA/OneDrive/Masaüstü/Turkcell/ML_Based_Sales_Prediction_API_Project/src/data/processed/sales_data.csv")

df.head(10)

# Harcama seviyesine göre segment oluşturma
df["segment"] = pd.qcut(df["total_sales"], q=3, labels=["Low", "Medium", "High"])


X = df.drop(columns=["customer_id", "segment", "order_date", "product_name"])  # Bağımsız değişkenler
y = df["segment"]  # Hedef değişken

# Kategorik verileri sayısal hale getirelim (One-Hot Encoding)
X = pd.get_dummies(X, drop_first=True)

# Kategorik değişkenleri sayısal hale getirme
le = LabelEncoder()
y = le.fit_transform(y)

# Eğitim ve test seti oluşturma (%80 eğitim, %20 test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Veriyi ölçekleme
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Modeli oluşturma ve eğitme
clf = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
clf.fit(X_train, y_train)

# Tahmin yapma
y_pred = clf.predict(X_test)

# Model başarı metriği
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Confusion Matrix
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# 3️⃣ Öğrenme eğrilerini hesapla
train_sizes, train_scores, test_scores = learning_curve(
    clf, X, y, cv=5, scoring="neg_mean_squared_error", train_sizes=np.linspace(0.1, 1.0, 10)
)

# 4️⃣ Ortalamaları al ve hata metriklerine çevir (MSE pozitif olmalı)
train_errors = -np.mean(train_scores, axis=1)
test_errors = -np.mean(test_scores, axis=1)

# 5️⃣ Grafik çiz
plt.figure(figsize=(8, 6))
plt.plot(train_sizes, train_errors, "o-", label="Eğitim Hatası", color="blue")
plt.plot(train_sizes, test_errors, "o-", label="Doğrulama Hatası", color="red")

plt.xlabel("Eğitim Veri Sayısı")
plt.ylabel("Hata (MSE)")
plt.title("Öğrenme Eğrisi (Learning Curve)")
plt.legend()
plt.grid(True)
plt.show()






from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

# Tahmin yapma
y_pred1 = model.predict(X_test)

# Model başarı metriği
print("Accuracy Decision tree:", accuracy_score(y_test, y_pred1))
print("Classification Report:\n", classification_report(y_test, y_pred1))

# Hedef değişkenin sınıf dağılımını kontrol edelim
print(df["segment"].value_counts())