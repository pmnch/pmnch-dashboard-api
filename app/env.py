import os

ONLY_PMNCH = os.getenv("ONLY_PMNCH", "").lower() == "true"
LOAD_FROM_LOCAL_PKL_FILE = os.getenv("LOAD_FROM_LOCAL_PKL_FILE", "").lower() == "true"
SAVE_TO_PKL_FILE = os.getenv("SAVE_TO_PKL_FILE", "").lower() == "true"
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
ACCESS_TOKEN_SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY")
AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
STAGE = os.getenv("STAGE", "")