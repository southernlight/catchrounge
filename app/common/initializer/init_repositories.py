from app.repository.user_repository import UserRepository
from app.repository.table_repository import TableRepository

def init_repositories(db):

    user_repo = UserRepository(db["user"])
    table_repo = TableRepository(db["table"])
    
    return {
        "user_repository": user_repo,
        "table_repository": table_repo
    }