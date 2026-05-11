import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "nexa_vote_secret_key")
    JWT_EXPIRES_HOURS = 2