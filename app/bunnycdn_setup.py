import os
from dotenv import load_dotenv

load_dotenv()

BUNNY_STORAGE_ZONE = os.getenv("BUNNY_STORAGE_ZONE")
BUNNY_API_KEY = os.getenv("BUNNY_API_KEY")
BUNNY_STORAGE_HOST = os.getenv("BUNNY_STORAGE_HOST")
BUNNY_CDN_URL = os.getenv("BUNNY_CDN_URL")
