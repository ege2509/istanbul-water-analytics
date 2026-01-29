import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_batch

# Database connection
conn = psycopg2.connect(
    dbname="istanbul-water-analytics",
    user="postgres",
    password="ege2509",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

dam_dict = {
    "omerli": 235371000,
    "darlik": 107500000,
    "elmali": 9600000,
    "terkos": 162241000,
    "alibey": 34143000,
    "buyukcekmece": 148943000,
    "sazlidere": 88730000,
    "istrancalar": 6231000,
    "kazandere": 17424000,
    "pabucdere": 58500000
}
try:

 

    df1 = pd.read_excel("consumption_cleaned_5.xlsx")

    df1_long = df1.melt(id_vars=['Tarih'],
                    var_name="dam_name",
                    value_vars=['Ömerli', 'Darlik', 'Elmali', 'Terkos', 'Alibey', 'B.çekmece', 'Sazlidere', 'Kazandere', 'Pabuçdere', 'ıstırancalar'],
                    value_name="precipitation_pct")

    df1_long["dam_name"] = df1_long["dam_name"].replace({
        "B.çekmece": "Büyükçekmece",
        "ıstırancalar": "Istrancalar"
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
    df1_long['Tarih'] = pd.to_datetime(df1_long['Tarih']).dt.normalize()
    df1_long = df1_long.rename(columns={'Tarih' : 'date'})

    df1_long['max_capacity'] = df1_long['dam_name'].map(dam_dict)

    df1_long['precipitation_m3'] = (df1_long['precipitation_pct'] / 100) * df1_long['max_capacity']

    df2 = df1[['Tarih', 'İstanbul günlük tüketim(m³/gün)']].copy()
    df2['Tarih'] = pd.to_datetime(df2['Tarih']).dt.normalize()

    df2 = df2.rename(columns={
        'İstanbul günlük tüketim(m³/gün)': 'consumption_m3', 'Tarih' : 'date'})
    df2['city_name'] = 'Istanbul'


    df3= pd.read_excel("occupancy_cleaned_5.xlsx")

    df3_long = df3.melt(id_vars= ['Tarih'], 
                    var_name="dam_name", 
                    value_vars=['Ömerli', 'Darlık', 'Elmalı', 'Terkos', 'Alibey', 'Büyükçekmece', 'Sazlıdere', 'Kazandere', 'Pabuçdere', 'Istrancalar'], 
                    value_name="occupancy_pct")

    cutoff = pd.Timestamp("1.01.2011  00:00:00")

    df4 = df3_long[df3_long['Tarih']  >= cutoff].copy() 

    df4["dam_name"] = (
        df4["dam_name"]
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("ü", "u")
        .str.replace("ö", "o")
        .str.replace("ç", "c")
        .str.replace("ğ", "g")
        .str.replace("ş", "s")
        .str.replace("ı", "i")
    )
    df4['Tarih'] = pd.to_datetime(df4['Tarih']).dt.normalize()
    df4 = df4.rename(columns={ 'Tarih' : 'date'})

    df4['max_capacity'] = df4['dam_name'].map(dam_dict)

    df4['occupancy_m3'] = (df4['occupancy_pct'] / 100) * df4['max_capacity']

    dams_data = [
        ("omerli", "235371000"),
        ("darlik", "107500000"),
        ("elmali", "9600000"),
        ("terkos", "162241000"),
        ("alibey", "34143000"),
        ("buyukcekmece", "148943000"),
        ("sazlidere", "88730000"),
        ("istrancalar", "6231000"),
        ("kazandere", "17424000"),
        ("pabucdere", "58500000")
    ]

    for dam_name, max_capacity in dams_data:
        cursor.execute(""" 
        INSERT INTO dams (dam_name, max_capacity_m3) 
        VALUES  (%s,%s)
        ON CONFLICT (dam_name) DO NOTHING
            """, (dam_name, max_capacity))   
        conn.commit()          
        print(f"Inserted {len(dams_data)} dams")


    cursor.execute("SELECT id, dam_name FROM dams")
    dam_id_map = {row[1]: row[0] for row in cursor.fetchall()}
    
    print(sorted(df1_long["dam_name"].unique()))
    print(sorted(df4["dam_name"].unique()))

    print("Merging precipitation and occupancy data...")
    df_combined = pd.merge(
        df1_long,
        df4,
        on=['dam_name', 'date'],
        how='outer'
    )
    
    print("Inserting daily dam data...")
    daily_dam_data = []
    for _, row in df_combined.iterrows():
        dam_id = dam_id_map.get(row['dam_name'])
        if dam_id:
            daily_dam_data.append((
                dam_id,
                row['date'],
                row.get('precipitation_m3'),
                row.get('occupancy_pct'),
                row.get('precipitation_pct'),
                row.get('occupancy_m3')
            ))
    
    execute_batch(cursor, """
        INSERT INTO daily_dam (dam_id, date, precipitation_m3, occupancy_pct, precipitation_pct, occupancy_m3)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, daily_dam_data)
    conn.commit()
    print(f"Inserted {len(daily_dam_data)} daily dam records")
    
    print("Inserting city consumption data...")
    city_consumption_data = [
        (row['city_name'], row['date'], row['consumption_m3'])
        for _, row in df2.iterrows()
        if pd.notna(row['consumption_m3'])
    ]
    
    execute_batch(cursor, """
        INSERT INTO city_consumption (city_name, date, consumption_m3)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
    """, city_consumption_data)
    conn.commit()
    print(f"Inserted {len(city_consumption_data)} city consumption records")
    
    print("\nAll data inserted successfully!")
    
except Exception as e:
    conn.rollback()
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    cursor.close()
    conn.close()