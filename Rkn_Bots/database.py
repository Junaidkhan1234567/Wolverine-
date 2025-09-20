from pymongo import MongoClient
from config import DB_URL, DB_NAME

client = MongoClient(DB_URL)
db = client[DB_NAME]
users_coll = db["users"]

def add_user(user_id: int):
    """अगर user नया है तो database में डालो"""
    if users_coll.count_documents({"user_id": user_id}, limit=1) == 0:
        users_coll.insert_one({"user_id": user_id})

def get_all_user_ids():
    """सभी user_ids की list लौटाओ"""
    return [d["user_id"] for d in users_coll.find({}, {"user_id": 1})]
