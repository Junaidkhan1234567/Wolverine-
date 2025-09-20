from pymongo import MongoClient
from config import DB_URL, DB_NAME
import motor.motor_asyncio
from config import Rkn_Bots

client = motor.motor_asyncio.AsyncIOMotorClient(Rkn_Bots.DB_URL)
db = client[Rkn_Bots.DB_NAME]
chnl_ids = db.chnl_ids
users = db.users

#insert user data
async def insert(user_id):
    user_det = {"_id": user_id}
    try:
        await users.insert_one(user_det)
    except:
        pass
        
# Total User
async def total_user():
    user = await users.count_documents({})
    return user

async def getid():
    all_users = users.find({})
    return all_users

async def delete(id):
    await users.delete_one(id)
                     
async def addCap(chnl_id, caption):
    dets = {"chnl_id": chnl_id, "caption": caption}
    await chnl_ids.insert_one(dets)

async def updateCap(chnl_id, caption):
    await chnl_ids.update_one({"chnl_id": chnl_id}, {"$set": {"caption": caption}})
client = MongoClient(DB_URL)
db = client[DB_NAME]
users_coll = db["users"]

def add_user(user_id: int):
    """अगर user नया है तो database में डालो"""
    if users_coll.count_documents({"user_id": user_id}, limit=1) == 0:
        users_coll.insert_one({"user_id": user_id})

def get_all_user_ids():
    return [d["user_id"] for d in users_coll.find({}, {"user_id": 1})]
