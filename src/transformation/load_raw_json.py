# src/transformation/load_raw_json.py

import os
import json
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# DB credentials from .env
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()

# Create schema if not exists
cursor.execute("CREATE SCHEMA IF NOT EXISTS raw;")
cursor.execute("""
CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    id BIGINT PRIMARY KEY,
    message TEXT,
    date TIMESTAMP,
    sender_id BIGINT,
    channel_name TEXT,
    raw_json JSONB
);
""")
conn.commit()

# Load JSON files
DATA_DIR = Path("data/raw/telegram_messages")

for date_dir in DATA_DIR.iterdir():
    for file in date_dir.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            messages = json.load(f)
        rows = []
        for msg in messages:
            rows.append((
                msg.get("id"),
                msg.get("message"),
                msg.get("date"),
                msg.get("from_id", {}).get("user_id"),
                file.stem,
                json.dumps(msg)
            ))

        df = pd.DataFrame(rows, columns=["id", "message", "date", "sender_id", "channel_name", "raw_json"])
        for _, row in df.iterrows():
            try:
                cursor.execute("""
                INSERT INTO raw.telegram_messages (id, message, date, sender_id, channel_name, raw_json)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
                """, row)
            except Exception as e:
                print("Error inserting row:", e)
conn.commit()
conn.close()
