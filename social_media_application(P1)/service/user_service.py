import secrets
from datetime import datetime, timedelta

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


    def forgot_password(self, email):

        user = self.user_dao.find_by_email(email)

        # Don't reveal whether email exists
        if not user:
            return True, "If the email exists, a reset link has been sent."

        token = secrets.token_urlsafe(32)

        user.reset_token = token

        user.reset_token_expiry = (
            datetime.utcnow() + timedelta(minutes=15)
        )

        self.user_dao.save_user(user)

        # For now we return the token.
        # Later we can send it through email.

        return True, token

    def reset_password(self, token, new_password):

        user = self.user_dao.get_user_by_reset_token(token)

        if not user:

            return False, "Invalid reset token"

        if not user.reset_token_expiry:

            return False, "Invalid reset token"

        if datetime.utcnow() > user.reset_token_expiry:

            return False, "Reset token has expired"

        if not new_password or len(new_password) < 6:

            return False, "Password must contain at least 6 characters"

        # Use the same password hashing method
        # that you already use during registration.

        user.password = generate_password_hash(new_password)

        # Token can be used only once
        user.reset_token = None
        user.reset_token_expiry = None

        self.user_dao.save_user(user)

        return True, "Password reset successfully"