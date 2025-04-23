# Müşterilerin alışveriş davranışlarına göre gruplanması ve aykırı verilerin keşfi 

# order_details

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import psycopg2
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator

user = "postgres"
password = "12345"
host = "localhost"
port = "5432"
database = "GYK1_Northwind"

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")

query = """
SELECT
    c.customer_id,
    COUNT(o.order_id) AS total_orders,
    SUM(od.unit_price * od.quantity) AS total_spent,
    AVG(od.unit_price * od.quantity) AS avg_order_value
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_details od ON o.order_id = od.order_id
GROUP BY c.customer_id
HAVING COUNT(o.order_id) > 0;


"""
df = pd.read_sql_query(query, engine)
print(df.head())

X = df[["total_orders", "total_spent", "avg_order_value"]]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

def find_optimal_eps(X_scaled,min_samples=3):
    neighbors = NearestNeighbors(n_neighbors=min_samples).fit(X_scaled)
    distances, _ =neighbors.kneighbors(X_scaled)

    distances = np.sort(distances[:, min_samples-1])

    kneedle = KneeLocator(range(len(distances)), distances, curve='convex', direction='increasing')
    optimal_eps = distances[kneedle.elbow]

    plt.figure(figsize=(10, 6))
    plt.plot(distances)
    plt.axvline(x=kneedle.elbow, color='r', linestyle='--', label=f'Optimal eps: {optimal_eps:.2f}')
    plt.xlabel('Points sorted by distance')
    plt.ylabel(f'{min_samples}-th nearest neighbor distance')
    plt.title('Elbow Method for Optimal eps')
    plt.legend()
    plt.grid(True)
    plt.show()

    return optimal_eps

optimal_eps = find_optimal_eps(X_scaled)
dbscan = DBSCAN(eps=optimal_eps, min_samples=3)
df['cluster'] = dbscan.fit_predict(X_scaled)

dbscan.fit_predict(X_scaled)

plt.figure(figsize=(10, 6))
plt.scatter(df['total_orders'], df['total_spent'], c=df['cluster'], cmap='plasma', s=60)
plt.xlabel("Toplam Sipariş Sayısı")
plt.ylabel("Toplam Harcama")
plt.title("Müşteri Segmentasyonu (DBSCAN)")
plt.grid(True)
plt.colorbar(label='Küme No')
plt.show()

outliers = df[df["cluster"] == -1]
print("Aykırı ver sayısı : ", len(outliers))
print(outliers[["customer_id", "total_orders", "total_spent"]])