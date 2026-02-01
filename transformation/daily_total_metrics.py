import pandas as pd
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)


def calculate_daily_system_metrics():
    cursor = conn.cursor()

    try:
        print("Calculating daily system metrics...")

        cursor.execute("SELECT SUM(max_capacity_m3) FROM dams")
        total_capacity = cursor.fetchone()[0]

        query = """
        WITH daily_aggregates AS (
            SELECT 
                dd.date,
                SUM(dd.precipitation_m3) as total_precipitation_m3,
                SUM(dd.occupancy_m3) as total_occupancy_m3,
                MAX(cc.consumption_m3) as total_consumption_m3
            FROM daily_dam dd
            LEFT JOIN city_consumption cc ON dd.date = cc.date
            GROUP BY dd.date
        )
        SELECT 
            date,
            total_precipitation_m3,
            total_occupancy_m3,
            total_consumption_m3,
            %s as total_capacity_m3
        FROM daily_aggregates
        ORDER BY date
        """
        
        cursor.execute(query, (total_capacity,))
        results = cursor.fetchall()
        

        inserted_count = 0
        for row in results:
            date, precip, occupancy, consumption, capacity = row

            precip = float(precip) if precip is not None else 0.0
            occupancy = float(occupancy) if occupancy is not None else 0.0
            consumption = float(consumption) if consumption is not None else 0.0
            capacity = float(capacity) if capacity is not None else 0.0
            
            
            system_occupancy_pct = (occupancy / capacity * 100) if capacity > 0 else 0.0
            net_change = precip - (consumption / 10)
            
            cursor.execute("""
                INSERT INTO daily_system_metrics 
                (date, total_precipitation_m3, total_occupancy_m3, total_capacity_m3, 
                 system_occupancy_pct, total_consumption_m3, net_change_m3)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (date) DO NOTHING
            """, (date, precip, occupancy, capacity, system_occupancy_pct, consumption, net_change))
            
            inserted_count += 1
        
        conn.commit()
        print(f" Inserted/updated {inserted_count} daily system metrics")
        
        cursor.execute("""
            SELECT 
                date, 
                total_precipitation_m3, 
                total_occupancy_m3, 
                system_occupancy_pct,
                CASE 
                    WHEN total_precipitation_m3 IS NULL THEN 'NULL'
                    ELSE 'OK'
                END as precip_status
            FROM daily_system_metrics
            ORDER BY date DESC
            LIMIT 10
        """)
        
        print("\n Sample Results (Latest 10 days):")
        print("-" * 100)
        print(f"{'Date':<12} | {'Precipitation (m³)':<20} | {'Occupancy (m³)':<20} | {'System %':<10} | {'Status':<10}")
        print("-" * 100)
        for row in cursor.fetchall():
            print(f"{str(row[0]):<12} | {row[1]:>20,.0f} | {row[2]:>20,.0f} | {row[3]:>9.2f}% | {row[4]:<10}")
        
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        cursor.close()

if __name__ == "__main__":
    calculate_daily_system_metrics()
    conn.close()
    print("\nDone!")