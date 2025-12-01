import os
from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")

USER_DATA_FILE = "data/user_data.json"

os.makedirs("data", exist_ok=True)
