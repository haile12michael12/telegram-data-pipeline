# src/ingestion/telegram_scraper.py

from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv
import os, json, logging
from datetime import datetime
from pathlib import Path

# Load .env
load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

# Configure logging
logging.basicConfig(
    filename="scrape.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

CHANNELS = {
    "lobelia4cosmetics": "https://t.me/lobelia4cosmetics",
    "tikvahpharma": "https://t.me/tikvahpharma"
}

DATA_PATH = Path("data/raw/telegram_messages")

def save_messages(messages, channel_name, date_str):
    DATA_PATH.joinpath(date_str).mkdir(parents=True, exist_ok=True)
    filepath = DATA_PATH / date_str / f"{channel_name}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

async def scrape_channel(client, channel_name, channel_link, limit=1000):
    try:
        messages_data = []
        async for msg in client.iter_messages(channel_link, limit=limit):
            message_dict = msg.to_dict()
            messages_data.append(message_dict)
        date_str = datetime.now().strftime("%Y-%m-%d")
        save_messages(messages_data, channel_name, date_str)
        logging.info(f"Scraped {len(messages_data)} messages from {channel_name}")
    except Exception as e:
        logging.error(f"Failed to scrape {channel_name}: {str(e)}")

async def main():
    async with TelegramClient("scraper_session", api_id, api_hash) as client:
        for name, link in CHANNELS.items():
            await scrape_channel(client, name, link)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
