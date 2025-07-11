# telegram_api/main.py

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from .database import SessionLocal
import schemas, crud

app = FastAPI(title="Telegram Analytical API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/reports/top-products", response_model=list[schemas.TopProduct])
def top_products(limit: int = Query(10, le=100), db: Session = Depends(get_db)):
    results = crud.get_top_products(db, limit)
    return [{"product": row[0], "count": row[1]} for row in results]

@app.get("/api/channels/{channel_name}/activity", response_model=list[schemas.ChannelActivity])
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    results = crud.get_channel_activity(db, channel_name)
    return [{"date": str(row[0]), "message_count": row[1]} for row in results]

@app.get("/api/search/messages", response_model=list[schemas.SearchResult])
def search_messages(query: str = Query(..., min_length=2), db: Session = Depends(get_db)):
    results = crud.search_messages(db, query)
    return [
        {
            "message_id": row[0],
            "channel_name": row[1],
            "date": str(row[2]),
            "message": row[3]
        } for row in results
    ]
