import pandas as pd
df1 = pd.read_excel("percipitation_consumption_cleaned.xlsx")

df1_long = df1.melt(id_vars=['Tarih'],
                    var_name="dam_name",
                    value_vars=['Ömerli', 'Darlik', 'Elmali', 'Terkos', 'Alibey', 'B.çekmece', 'Sazlidere', 'Kazandere', 'Pabuçdere', 'ıstırancalar'])
df2 = df1[['Tarih', 'İstanbul günlük tüketim(m³/gün)']]


