import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/lead_rescue")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
    SLACK_CHANNELS = {
        "hot": os.getenv("SLACK_CHANNEL_HOT", ""),
        "warm": os.getenv("SLACK_CHANNEL_WARM", ""),
        "cold": os.getenv("SLACK_CHANNEL_COLD", ""),
    }
    ALERT_EMAIL = os.getenv("ALERT_EMAIL", "admin@example.com")

settings = Settings()
