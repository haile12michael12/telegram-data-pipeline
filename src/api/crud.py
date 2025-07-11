# telegram_api/crud.py

from sqlalchemy.orm import Session
from fastapi import HTTPException

def get_top_products(db: Session, limit: int = 10):
    query = """
        SELECT LOWER(word) AS product, COUNT(*) AS count
        FROM (
            SELECT unnest(string_to_array(message, ' ')) AS word
            FROM analytics.fct_messages
            WHERE message IS NOT NULL
        ) sub
        GROUP BY word
        ORDER BY count DESC
        LIMIT %s;
    """
    return db.execute(query, (limit,)).fetchall()

def get_channel_activity(db: Session, channel_name: str):
    query = """
        SELECT date::date, COUNT(*) as message_count
        FROM analytics.fct_messages
        WHERE channel_name = %s
        GROUP BY date::date
        ORDER BY date::date;
    """
    results = db.execute(query, (channel_name,)).fetchall()
    if not results:
        raise HTTPException(status_code=404, detail="Channel not found")
    return results

def search_messages(db: Session, keyword: str):
    query = """
        SELECT message_id, channel_name, date, message
        FROM analytics.fct_messages
        WHERE message ILIKE %s
        ORDER BY date DESC
        LIMIT 50;
    """
    return db.execute(query, (f'%{keyword}%',)).fetchall()
