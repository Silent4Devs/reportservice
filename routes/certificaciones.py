import pandas as pd
import xlrd


df=pd.read_excel('inventario.xlsx', engine='openpyxl')

df.dropna(inplace=True)
df.drop_duplicates(inplace=True)
print(df)