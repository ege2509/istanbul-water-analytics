import pandas as pd
df1 = pd.read_excel("percipitation_consumption_cleaned.xlsx")

df1_long = df1.melt(id_vars=['Tarih'],
                    var_name="dam_name",
                    value_vars=['Ömerli', 'Darlik', 'Elmali', 'Terkos', 'Alibey', 'B.çekmece', 'Sazlidere', 'Kazandere', 'Pabuçdere', 'ıstırancalar'])

df1_long = df1_long.rename(columns={
    'ıstırancalar': 'Istrancalar', 'B.çekmece': 'Buyukcekmece'
})

df1_long["dam_name"] = (
    df1_long["dam_name"]
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("ü", "u")
    .str.replace("ö", "o")
    .str.replace("ç", "c")
    .str.replace("ğ", "g")
    .str.replace("ş", "s")
    .str.replace("ı", "i")
)

df1_long = df1_long.rename(columns={'Tarih' : 'Date'})

df2 = df1[['Tarih', 'İstanbul günlük tüketim(m³/gün)']]

df2 = df2.rename(columns={
    'İstanbul günlük tüketim(m³/gün)': 'city_daily_consumption_m3', 'Tarih' : 'Date'
})
