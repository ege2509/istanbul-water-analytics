import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_batch

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


def visualise_occupancy():
    cursor = conn.cursor()
    df = pd.read_sql("SELECT", conn)
    
