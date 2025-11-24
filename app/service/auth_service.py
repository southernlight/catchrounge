import hashlib
import jwt
from datetime import datetime, timedelta

class AuthService:

    def __init__(self, user_repository,secret_key):
        self.user_repository = user_repository
        self.secret_key = secret_key

    def signup(self, username, password, phone):

        if self.user_repository.find_by_username(username):
            return False, "이미 사용 중인 username입니다."
        
        self.user_repository.save(username, password, phone)
        return True, "회원가입 성공"

    def signin(self, username, password):

        user = self.user_repository.find_by_username(username)
        if not user:
            return None
        
        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if user["password"] != password_hash:
            return None

        payload = {
            "username": username,
            "exp": datetime.utcnow() + timedelta(days=1)
        }
        
        return jwt.encode(payload, self.secret_key, algorithm="HS256")