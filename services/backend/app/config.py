import os
from dotenv import load_dotenv

load_dotenv()

# Rasa URL (adjust if running on different port/machine)
RASA_BASE_URL = os.getenv("RASA_BASE_URL", "http://localhost:5005")

# SQLite database file
SQLITE_DB = os.getenv("SQLITE_DB", "subscribers.db")

# Google Gemini API key (from .env)
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "")
