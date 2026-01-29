import pandas as pd

df1 = pd.read_excel('data/raw/istanbul-dams-daily-occupancy-rates.xlsx')
df1['Tarih'] = pd.to_datetime(df1['Tarih'], dayfirst= True, errors = 'coerce')

df1['Tarih'] = df1['Tarih'].dt.normalize()

print(f"Failed conversions: {df1['Tarih'].isnull().sum()}")


df2 = pd.read_excel('data/raw/istanbul-barajlarnda-ya-ve-gunluk-tuketim-verileri.xlsx')
df2 = df2.drop(columns=['Unnamed: 11'])


problem_start = pd.Timestamp('2023-04-01')
problem_end = pd.Timestamp('2023-08-08')


mask = (df1['Tarih'] >= problem_start) & (df1['Tarih'] <= problem_end)

dam_cols = df1.columns.drop('Tarih')

df1[dam_cols] = df1[dam_cols].apply(pd.to_numeric, errors='coerce')

df1.loc[mask, dam_cols] = df1.loc[mask, dam_cols] / 100

df1.loc[mask].head()



df1.to_excel('occupancy_cleaned_5.xlsx', index=False)
df2.to_excel('consumption_cleaned_5.xlsx', index=False)



