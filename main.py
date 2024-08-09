import logging
from pyrogram import Client, filters
from bot.handlers import start, download_reel
from bot.utils import is_admin, broadcast_message
from bot.db import setup_mongo

# Load environment variables
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and MongoDB
app = Client("instagram_reels_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
db = setup_mongo(MONGO_URI)

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    await start(client, message)

@app.on_message(filters.command("download"))
async def download_handler(client, message):
    await download_reel(client, message, db)

@app.on_message(filters.command("broadcast") & filters.user(is_admin))
async def broadcast_handler(client, message):
    await broadcast_message(client, message, db)

# Log incoming messages
@app.on_message(filters.all)
async def log_all_messages(client, message):
    await client.send_message(LOG_CHANNEL, f"Received message from {message.from_user.id}: {message.text}")

if __name__ == "__main__":
    app.run()
