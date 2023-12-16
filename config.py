import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URL = os.environ["SQLALCHEMY_DATABASE_URL"]
    TIMEPAD_API_URL = "https://ontp.timepad.ru/api/events{params}"
