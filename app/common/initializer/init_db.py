from pymongo import MongoClient
import logging

mongo_client = None
db = None

def init_db(app):

    global mongo_client, db
    mongo_uri = app.config.get("MONGO_URI")
    logging.info(f"Connecting to MongoDB at: {mongo_uri}")
    mongo_client = MongoClient(mongo_uri)
    db_name = app.config.get("DB_NAME")
    db = mongo_client[db_name]
    return db

def init_tables(db):
    table_collection = db["table"]
    
    if table_collection.count_documents({}) == 0:
        tables = [{"tableNum": i, "occupied": False, "user_name": None, "time": None} for i in range(1, 19)]
        table_collection.insert_many(tables)

def get_db_client():
    global mongo_client
    return mongo_client