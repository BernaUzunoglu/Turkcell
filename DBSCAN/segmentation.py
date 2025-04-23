import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator
from config import Config

engine = create_engine(Config.DATABASE_URL)

def get_segmented_data():
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
    X = df[["total_orders", "total_spent", "avg_order_value"]]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    neighbors = NearestNeighbors(n_neighbors=3).fit(X_scaled)
    distances, _ = neighbors.kneighbors(X_scaled)
    distances = np.sort(distances[:, 2])
    kneedle = KneeLocator(range(len(distances)), distances, curve='convex', direction='increasing')
    optimal_eps = distances[kneedle.elbow]

    dbscan = DBSCAN(eps=optimal_eps, min_samples=3)
    df["cluster"] = dbscan.fit_predict(X_scaled)

    return df
