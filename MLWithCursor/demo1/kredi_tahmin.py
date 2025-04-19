import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Rastgele veri oluşturma
np.random.seed(42)

# 50 örnek için veri oluşturma
n_samples = 50

# Özellikler:
# 1. Yaş (18-65 arası)
# 2. Aylık Gelir (1000-10000 arası)
# 3. Kredi Puanı (300-850 arası)
# 4. Borç/Gelir Oranı (0.1-0.8 arası)
# 5. Kredi Geçmişi (0-1 arası, 1: iyi geçmiş)

# Veri oluşturma
ages = np.random.randint(18, 65, n_samples)
incomes = np.random.randint(1000, 10000, n_samples)
credit_scores = np.random.randint(300, 850, n_samples)
debt_ratios = np.random.uniform(0.1, 0.8, n_samples)
credit_histories = np.random.randint(0, 2, n_samples)

# Hedef değişken (Kredi Onayı: 1: Onaylandı, 0: Reddedildi)
# Kredi puanı yüksek, borç oranı düşük ve kredi geçmişi iyi olanların onaylanma olasılığı daha yüksek
approvals = np.zeros(n_samples)
for i in range(n_samples):
    if (credit_scores[i] > 650 and 
        debt_ratios[i] < 0.5 and 
        credit_histories[i] == 1):
        approvals[i] = 1

# DataFrame oluşturma
data = pd.DataFrame({
    'Yaş': ages,
    'Aylık_Gelir': incomes,
    'Kredi_Puanı': credit_scores,
    'Borç_Oranı': debt_ratios,
    'Kredi_Geçmişi': credit_histories,
    'Onay': approvals
})

# Veriyi görselleştirme
plt.figure(figsize=(12, 8))
sns.pairplot(data, hue='Onay')
plt.savefig('demo1/veri_görselleştirme.png')
plt.close()

# Veriyi özellikler ve hedef olarak ayırma
X = data.drop('Onay', axis=1)
y = data['Onay']

# Veriyi eğitim ve test setlerine ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Veriyi ölçeklendirme
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Modelleri tanımlama
models = {
    'KNN': KNeighborsClassifier(n_neighbors=5),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(kernel='rbf', random_state=42)
}

# Her model için performans değerlendirmesi
results = {}
for name, model in models.items():
    # Modeli eğitme
    model.fit(X_train_scaled, y_train)
    
    # Tahmin yapma
    y_pred = model.predict(X_test_scaled)
    
    # Performans metriklerini hesaplama
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    results[name] = {
        'accuracy': accuracy,
        'report': report
    }
    
    print(f"\n{name} Modeli Sonuçları:")
    print(f"Doğruluk: {accuracy:.2f}")
    print("Sınıflandırma Raporu:")
    print(report)

# En iyi modeli belirleme
best_model = max(results, key=lambda x: results[x]['accuracy'])
print(f"\nEn iyi performans gösteren model: {best_model}")
print(f"Doğruluk: {results[best_model]['accuracy']:.2f}")

# Önemli özellikleri görselleştirme (Random Forest için)
if best_model == 'Random Forest':
    rf_model = models['Random Forest']
    feature_importance = pd.DataFrame({
        'Özellik': X.columns,
        'Önem': rf_model.feature_importances_
    }).sort_values('Önem', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Önem', y='Özellik', data=feature_importance)
    plt.title('Özellik Önemleri')
    plt.savefig('demo1/özellik_önemleri.png')
    plt.close() 