import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator
from config import Config

engine = create_engine(Config.DATABASE_URL)

def get_product_clusters():
    query = """
    SELECT
        p.product_id,
        AVG(od.unit_price) AS avg_price,
        COUNT(od.order_id) AS order_count,
        AVG(od.quantity) AS avg_quantity_per_order,
        COUNT(DISTINCT o.customer_id) AS distinct_customers
    FROM products p
    INNER JOIN order_details od ON p.product_id = od.product_id
    INNER JOIN orders o ON od.order_id = o.order_id
    GROUP BY p.product_id
    HAVING COUNT(od.order_id) > 0;
    """
    df = pd.read_sql_query(query, engine)

    features = df[["avg_price", "order_count", "avg_quantity_per_order", "distinct_customers"]]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    neighbors = NearestNeighbors(n_neighbors=3).fit(X_scaled)
    distances, _ = neighbors.kneighbors(X_scaled)
    distances = np.sort(distances[:, 2])
    kneedle = KneeLocator(range(len(distances)), distances, curve='convex', direction='increasing')
    optimal_eps = distances[kneedle.elbow]

    dbscan = DBSCAN(eps=optimal_eps, min_samples=3)
    df["cluster"] = dbscan.fit_predict(X_scaled)

    return df
