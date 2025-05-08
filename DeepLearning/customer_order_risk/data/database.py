import pandas as pd
import psycopg2
from DeepLearning.customer_order_risk.config import DB_CONFIG

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            print("Database connection established")
        except Exception as e:
            print(f"Error connecting to the database :{e}")
            raise

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("Connection closed")

    def get_order_data(self):
        query = """
        SELECT 
            od.order_id,
            od.product_id,
            od.unit_price,
            od.quantity,
            od.discount,
            o.customer_id,
            o.order_date,
            p.category_id,
            c.company_name
                FROM orders o
                INNER JOIN order_details od ON o.order_id = od.order_id
                INNER JOIN products p ON p.product_id = od.product_id
                INNER JOIN customers c ON c.customer_id = o.customer_id 
        """
        try:
            df = pd.read_sql(query, self.conn)
            return df
        except Exception as e:
            print(f"Error {e}")
            raise


