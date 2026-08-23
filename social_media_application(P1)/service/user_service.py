from werkzeug.security import generate_password_hash, check_password_hash
from dao.user_dao import UserDAO


class UserService:

    def __init__(self):
        self.user_dao = UserDAO()

    def register_user(self, username, email, password):

        if not username or not email or not password:
            return False, "All fields are required"

        existing_email = self.user_dao.find_by_email(email)

        if existing_email:
            return False, "Email already registered"

        existing_username = self.user_dao.find_by_username(username)

        if existing_username:
            return False, "Username already exists"

        hashed_password = generate_password_hash(password)

        self.user_dao.create_user(
            username,
            email,
            hashed_password
        )

        return True, "Registration successful"


    def login_user(self, email, password):

        user = self.user_dao.find_by_email(email)

        if not user:
            return False, "Invalid email or password"

        if not check_password_hash(user.password, password):
            return False, "Invalid email or password"

        return True, user

    def get_user_by_id(self, user_id):

        return self.user_dao.get_user_by_id(user_id)

    def get_all_users(self):

        return self.user_dao.get_all_users()
    

    def create_admin(self, username, email, password, role):

        existing_user = self.user_dao.find_by_email(email)

        if existing_user:
            return False, "User with this email already exists"

        hashed_password = generate_password_hash(password)

        self.user_dao.create_user(username, email, hashed_password,role)

        return True, "Admin created successfully"