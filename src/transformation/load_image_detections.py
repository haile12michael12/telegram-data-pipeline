# src/transformation/load_image_detections.py

import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("CREATE SCHEMA IF NOT EXISTS raw;")
cursor.execute("""
CREATE TABLE IF NOT EXISTS raw.image_detections (
    message_id BIGINT,
    channel_name TEXT,
    detected_object_class TEXT,
    confidence_score FLOAT
);
""")
conn.commit()

# Load detections
df = pd.read_csv("data/processed/image_detections.csv")

for _, row in df.iterrows():
    cursor.execute("""
    INSERT INTO raw.image_detections (message_id, channel_name, detected_object_class, confidence_score)
    VALUES (%s, %s, %s, %s)
    """, tuple(row))
conn.commit()
conn.close()
