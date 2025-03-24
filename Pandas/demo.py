import pandas as pd

# Series - Tek boyutu diziler
# DataFrame - Tablolar

dailySales = pd.Series([1500,2500,3500,200,1500,1000,6000])
print(dailySales)

print("Index: ", dailySales)
print("Values : ", dailySales.values)
print("Mean : ", dailySales.mean())
print("Max : ", dailySales.max())
print("Min : ", dailySales.min())

# indexle veriye erişme
print(dailySales[3])

days= [ "Monday","Tuesday","wednesday","Thursday","Friday","Saturday","Sunday"]
dailySales2 = pd.Series([1500,2500,3500,200,1500,1000,6000],index = days)
print(dailySales2["Thursday"])


salesData = {
    "ProductName":["Elma","Armut","Üzüm","İncir","Portakal","Elma","Elma","Portakal"],
    "Price":[200,100,500,300,40,50,120,120],
    "QuantitySold":[20,3,5,8,9,14,26,12],
}

df = pd.DataFrame(salesData)
print(df)

print(df["ProductName"])
print(type(df["ProductName"]))
print(df["Price"].mean())

print(type(df[["ProductName","Price"]]))

print(df.iloc[2])
print(type(df.iloc[2]))

print(df.loc[df["ProductName"] == "İncir"])

bestSales = df[df["QuantitySold"]>10]
print(bestSales)

df["Total"] = df["Price"]*df["QuantitySold"]
print(df)

print(df.groupby("ProductName")["QuantitySold"].sum())


# Eksik veriler üzerinde çalışma
# Eksik değerler iş problemimize göre üzerinde işlem yapılır.
salesData2 = {
    "ProductName":["Elma","Armut","Üzüm","İncir","Portakal","Elma","Elma","Portakal"],
    "Price":[200,100,500,300,None,50,None,120],
    "QuantitySold":[20,3,None,8,9,14,26,12],
}

df = pd.DataFrame(salesData2)

print(df.isnull().sum())

df["Price"].fillna(df["Price"].mean(),inplace=True)
print(df)

df.dropna(inplace=True)
print(df)

print(df.sort_values("Price",ascending=True))

df.to_csv("Pandas/salesDataAnalysis.csv",index=False)
df.to_excel("Pandas/salesDataAnalysis.xlsx",index=False)