import pandas as pd
import numpy as np
import psycopg2
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# Connect to the database
connection = psycopg2.connect(
    host="localhost",
    dbname="GYK1_Northwind",
    user="postgres",
    password="12345",
    port="5432"
)

query = """
WITH last_order_date AS (
    SELECT MAX(order_date) AS max_date 
    FROM orders
),
customer_order_stats AS (
    SELECT 
        c.customer_id,
        COUNT(o.order_id) AS total_orders,
        SUM(od.unit_price * od.quantity) AS total_spent,
        AVG(od.unit_price * od.quantity) AS avg_order_value
    FROM orders o
    INNER JOIN customers c ON o.customer_id = c.customer_id
    INNER JOIN order_details od ON od.order_id = o.order_id
    GROUP BY c.customer_id
),
label_date AS (
    SELECT 
        c.customer_id,
        CASE 
            WHEN EXISTS (
                SELECT 1 
                FROM orders o2
                CROSS JOIN last_order_date lod
                WHERE o2.customer_id = c.customer_id
                  AND o2.order_date > (lod.max_date - INTERVAL '6 months')
            )
            THEN 1 ELSE 0 
        END AS will_order_again
    FROM customers c
)

SELECT s.customer_id,
s.total_orders,
s.total_spent,
s.avg_order_value,
l.will_order_again
FROM customer_order_stats s 
JOIN label_date l 
ON s.customer_id = l.customer_id;

"""

df = pd.read_sql(query, connection)
connection.close()

X = df[["total_orders", "total_spent", "avg_order_value"]]
y = df["will_order_again"]

# Özellikleri (X) ölçekle
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Veriyi eğitim ve test olarak ayır
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

model = tf.keras.Sequential(
    [
        tf.keras.layers.Dense(8,activation="relu", input_shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(4,activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid")
    ]
)
model.compile(optimizer="adam", loss="mean_squared_error", metrics=["accuracy"])
model.fit(X_train, y_train, epochs=50, validation_data=(X_test, y_test), verbose=1)

loss, acc = model.evaluate(X_test, y_test)
print(acc)












