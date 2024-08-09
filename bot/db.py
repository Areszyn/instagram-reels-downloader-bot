from pymongo import MongoClient

def setup_mongo(uri):
    client = MongoClient(uri)
    db = client["instagram_reels_bot"]
    return db
