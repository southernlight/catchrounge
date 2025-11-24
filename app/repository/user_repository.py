import hashlib

class UserRepository:

    def __init__(self, user_collection):
        self.user_collection = user_collection

    def find_by_username(self, username):
        return self.user_collection.find_one({"username": username}, {"_id": 0})
    
    def find_by_username(self, username, session=None):
            # find_one에 session=session 인자를 추가
            return self.user_collection.find_one(
                {"username": username}, 
                {"_id": 0},
                session=session 
            )

    def save(self, username, password, phone):
        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        doc = {
            "username": username,
            "password": password_hash,
            "phone": phone,
            "is_reserved": 0
        }
        self.user_collection.insert_one(doc)

    def update_user(self, username, update_fields: dict):
        self.user_collection.update_one(
            {"username": username},
            {"$set": update_fields}
        )

    def update_user(self, username, update_fields: dict, session=None):
        self.user_collection.update_one(
            {"username": username},
            {"$set": update_fields},
            session=session
        )
    