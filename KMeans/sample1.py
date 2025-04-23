import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Müşterilerin gelirleri ve harcmaları listesi
X = np.array([
    [20, 25], [22, 28], [19, 24], [21, 26], [23, 30],     # Düşük gelir, düşük harcama
    [50, 60], [52, 58], [48, 65], [53, 63], [51, 59],     # Orta gelir, orta harcama
    [90, 80], [95, 85], [92, 78], [88, 83], [93, 90],     # Yüksek gelir, yüksek harcama
    [80, 40], [85, 38], [78, 35], [83, 37],               # Yüksek gelir, düşük harcama
    [25, 60], [22, 65], [28, 70], [30, 68]                # Düşük gelir, yüksek harcama
])

# Farklı k değerleri için inertia'ları hesapla
inertias = []
k_values = range(1, 11)

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)

# Elbow grafiğini çiz
plt.figure(figsize=(8, 5))
plt.plot(k_values, inertias, marker='o')
plt.title('Elbow Yöntemi ile Optimal Kümeyi Belirleme')
plt.xlabel('Küme Sayısı (k)')
plt.ylabel('Inertia (Toplam Kare Hata)')
plt.xticks(k_values)
plt.grid(True)
plt.show()



kmeans = KMeans(n_clusters=4,random_state=42)

kmeans.fit(X)
labels = kmeans.labels_

plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='rainbow')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=200, marker='X', c='black')
plt.xlabel("Gelir")
plt.ylabel("Harcama")
plt.title("K-means ile Müşteri Segmentasyonu")
plt.show()