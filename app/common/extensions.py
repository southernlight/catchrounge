from pymongo import MongoClient

mongo_client = None
db = None

def init_mongo(app):

    global mongo_client, db
    mongo_uri = app.config.get("MONGO_URI", "mongodb://localhost:27017/")
    mongo_client = MongoClient(mongo_uri)
    db_name = app.config.get("MONGO_DB_NAME", "mydatabase")
    db = mongo_client[db_name]
    return db