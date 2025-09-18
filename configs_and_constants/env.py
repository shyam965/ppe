import os
from dotenv import load_dotenv

load_dotenv()

class Env:
    @staticmethod
    def get(key: str, default=None):
        return os.getenv(key, default)

env = Env()