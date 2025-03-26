import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
# C:\Users\BERNA\OneDrive\Masaüstü\Turkcell\ML_Based_Sales_Prediction_API_Project\src\data\processed\sales_data.csv

df = pd.read_csv("C:/Users/BERNA/OneDrive/Masaüstü/Turkcell/ML_Based_Sales_Prediction_API_Project/src/data/processed/sales_data.csv")
print(df.head(10))
