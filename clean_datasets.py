import pandas as pd

df1 = pd.read_excel('istanbul-dams-daily-occupancy-rates.xlsx')
df1['Tarih'] = pd.to_datetime(df1['Tarih'], errors = 'coerce')

print(f"Failed conversions: {df1['Tarih'].isnull().sum()}")


df2 = pd.read_excel('istanbul-barajlarnda-ya-ve-gunluk-tuketim-verileri.xlsx')
df2 = df2.drop(columns=['Unnamed: 11'])



df1.to_excel('occupancy_cleaned.xlsx', index=False)
df2.to_excel('consumption_cleaned.xlsx', index=False)
