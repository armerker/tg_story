import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = "8332906555:AAGTC35KXCCgnZoUsppyr5n0qBR_DU1EgcQ"
USER_DATA_FILE = "data/user_data.json"

# Создаем папки если их нет
os.makedirs("data", exist_ok=True)