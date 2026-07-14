from pyrogram import Client

import config
from database import Database

db = Database()

app = Client(
    name="MovieBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="plugins")
)

app.db = db

print("Bot Started...")

app.run()