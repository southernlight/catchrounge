class UserService:

    def __init__(self,user_repository):
        self.user_repository = user_repository

    def get_user_info(self, username):

        user = self.user_repository.find_by_username(username)
        if not user:
            return None
        return {
            "username": user["username"],
            "phone": user["phone"],
            "is_reserved": user["is_reserved"]
        }