from src.dao.user_dao import UserDAO

class UserService:
    def __init__(self):
        self.dao = UserDAO()

    def register_user(self, name, email, phone):
        return self.dao.register(name, email, phone)

    def get_user(self, email):
        return self.dao.get_by_email(email)

    def list_users(self):
        return self.dao.get_all()
