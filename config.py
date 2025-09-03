import os
from dotenv import load_dotenv

load_dotenv()

# Telegram API
API_ID = int(os.getenv("API_ID", 6435225))  
API_HASH = os.getenv("API_HASH", "4e984ea35f854762dcde906dce426c2d")

# Bot Token / String Session
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
STRING1 = os.getenv("STRING_SESSION", None)
PORT = int(os.environ.get("PORT", 10000))  # Render or UptimeRobot port


# Database
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://pusers:nycreation@nycreation.pd4klp1.mongodb.net/?retryWrites=true&w=majority&appName=NYCREATION")

# Owner / Admin
OWNER_ID = int(os.getenv("OWNER_ID", 7574330905))
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "WTF_WhyMeeh")

# Support / Updates
SUPPORT_GRP = os.getenv("SUPPORT_GRP", "ShrutiBotSupport")
UPDATE_CHNL = os.getenv("UPDATE_CHNL", "ShrutiBots")
