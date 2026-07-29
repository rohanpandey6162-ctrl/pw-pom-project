"""
Central config loader. Reads from environment variables / .env file
so credentials and URLs never get hardcoded in tests.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL = os.getenv("BASE_URL", "https://example.com")
    BROWSER = os.getenv("BROWSER", "chromium")  # chromium | firefox | webkit
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", "10000"))
    USERNAME = os.getenv("TEST_USERNAME", "")
    PASSWORD = os.getenv("TEST_PASSWORD", "")
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))
