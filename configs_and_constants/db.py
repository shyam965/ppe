import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv("DB_URI")
DB_NAME = os.getenv("DB_NAME")

client = pymongo.MongoClient(DB_URI)
db = client[DB_NAME]

print(f"[MongoDB] Connected to database: {DB_NAME}")