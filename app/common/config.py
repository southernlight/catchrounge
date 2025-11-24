import os
from dotenv import load_dotenv
import logging

ENVIRONMENT = os.getenv('ENVIRONMENT')
logging.info(f"DEBUG - Current ENVIRONMENT: {ENVIRONMENT}")

if ENVIRONMENT == 'docker':
    pass
else:
    load_dotenv('.env.local')

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")
