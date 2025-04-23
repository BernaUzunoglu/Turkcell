import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator
from config import Config

engine = create_engine(Config.DATABASE_URL)

def cluster_suppliers():
    query = """
    SELECT 
        s.supplier_id,
        COUNT(p.product_id) AS product_count,
        SUM(od.quantity) AS total_quantity,
        AVG(od.unit_price) AS avg_price,
        AVG(customer_count) AS avg_customers
    FROM suppliers s
    JOIN products p ON s.supplier_id = p.supplier_id
    JOIN order_details od ON p.product_id = od.product_id
    JOIN (
        SELECT od.product_id, COUNT(DISTINCT o.customer_id) AS customer_count
        FROM order_details od
        JOIN orders o ON od.order_id = o.order_id
        GROUP BY od.product_id
    ) product_customers ON product_customers.product_id = p.product_id
    GROUP BY s.supplier_id
    """

    df = pd.read_sql_query(query, engine)
    features = df[["product_count", "total_quantity", "avg_price", "avg_customers"]]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    neighbors = NearestNeighbors(n_neighbors=3).fit(X_scaled)
    distances, _ = neighbors.kneighbors(X_scaled)
    distances = sorted(distances[:, 2])
    kneedle = KneeLocator(range(len(distances)), distances, curve='convex', direction='increasing')
    optimal_eps = distances[kneedle.elbow]

    dbscan = DBSCAN(eps=optimal_eps, min_samples=3)
    df["cluster"] = dbscan.fit_predict(X_scaled)

    return df
