import os
from dotenv import load_dotenv

# Load environment variables from the root .env file
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(ROOT_DIR, ".env")

load_dotenv(ENV_FILE)

APP_NAME = os.getenv("APP_NAME", "LegalEase")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

MAX_DOCUMENT_LENGTH = int(
    os.getenv("MAX_DOCUMENT_LENGTH", "30000")
)
