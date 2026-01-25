DAM_MAX_CAPACITY = {
    "Ömerli": 235371000,
    "Darlik": 107500000,
    "Elmali ": 9600000,
    "Terkos": 162241000,
    "Alibey": 34143000,
    "Büyükçekmece": 148943000,
    "Sazlidere": 88730000,
    "Istrancalar": 6231000,
    "Kazandere": 17424000,
    "Pabuçdere": 58500000
}

import pandas as pd

df1 = pd.read_excel("occupancy_cleaned.xlsx")

df1_long = df1.melt(id_vars= ['Tarih'], 
                  var_name="dam_name", 
                  value_vars=['Ömerli', 'Darlık', 'Elmalı', 'Terkos', 'Alibey', 'Büyükçekmece', 'Sazlıdere', 'Kazandere', 'Pabuçdere', 'Istrancalar'], 
                  value_name="occupancy_pct")

cutoff = pd.Timestamp("1.01.2011  00:00:00")

df2 = df1_long[df1_long['Tarih']  >= cutoff].copy() 

df2["dam_name"] = (
    df2["dam_name"]
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("ü", "u")
    .str.replace("ö", "o")
    .str.replace("ç", "c")
    .str.replace("ğ", "g")
    .str.replace("ş", "s")
    .str.replace("ı", "i")
)

df2 = df2.rename(columns={ 'Tarih' : 'Date'})


