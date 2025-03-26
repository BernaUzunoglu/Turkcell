
def check_df(dataframe, head=5):
    print("############### Shape  ###############")
    print(dataframe.shape)
    print("############### Types  ###############")
    print(dataframe.dtypes)
    print("############### Head  ###############")
    print(dataframe.head(head))
    print("############### Tail  ###############")
    print(dataframe.tail(head))
    print("############### NA  ###############")
    print(dataframe.isnull().sum())
    print("############### Quantiles  ###############")
    print(dataframe.describe([0, 0.85, 0.50, 0.95, 0.99, 1]))  # bir pandas DataFrame içindeki sayısal veriler için özet istatistikleri hesaplar
    print("############### Null Datas  ###############")
    print(dataframe.isnull().head())