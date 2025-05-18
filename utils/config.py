
from dotenv import load_dotenv
import os

load_dotenv()

def validate_env():
    required_vars = ["GEMINI_API_KEY", "GOOGLE_MAPS_API_KEY", "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")