import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator
from config import Config

engine = create_engine(Config.DATABASE_URL)

def cluster_countries():
    query = """
    SELECT
        c.country,
        COUNT(o.order_id) AS total_orders,
        AVG(od.unit_price * od.quantity) AS avg_order_value,
        AVG(od.quantity) AS avg_items_per_order
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_details od ON o.order_id = od.order_id
    GROUP BY c.country
    """

    df = pd.read_sql_query(query, engine)
    features = df[["total_orders", "avg_order_value", "avg_items_per_order"]]

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
