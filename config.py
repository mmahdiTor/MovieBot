import os

from dotenv import load_dotenv

load_dotenv()


API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")


ADMINS = [
    int(x.strip())
    for x in os.getenv("ADMINS").split(",")
]


MOVIE_CHANNEL = int(os.getenv("MOVIE_CHANNEL"))


FORCE_SUB_CHANNELS = [
    x.strip()
    for x in os.getenv("FORCE_SUB_CHANNELS").split(",")
]


AUTO_DELETE_TIME = int(
    os.getenv("AUTO_DELETE_TIME")
)