import os
from dotenv import load_dotenv

load_dotenv()

GHL_ACCESS_TOKEN = os.getenv("GHL_ACCESS_TOKEN")
GHL_LOCATION_ID = os.getenv("GHL_LOCATION_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
