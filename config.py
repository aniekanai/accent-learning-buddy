# config.py

from dotenv import load_dotenv
import os

load_dotenv("api_keys.env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MURF_API_KEY = os.getenv("MURF_API_KEY")
