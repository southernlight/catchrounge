class TableRepository:
    def __init__(self, collection):
        self.collection = collection

    def find_all_tables(self):
        return list(self.collection.find({},{"_id": 0}))
    
    def find_by_table_num(self, table_num):
        return self.collection.find_one({"tableNum": table_num}, {"_id": 0})
    
    def find_by_table_num(self, table_num, session=None):
        return self.collection.find_one(
            {"tableNum": table_num}, 
            {"_id": 0},
            session=session 
        )
    
    def update_table(self, table_num, update_fields):
        self.collection.update_one(
            {"tableNum": table_num},
            {"$set": update_fields},
        )

    def update_table(self, table_num, update_fields,session=None):
        self.collection.update_one(
            {"tableNum": table_num},
            {"$set": update_fields},
            session=session
        )
