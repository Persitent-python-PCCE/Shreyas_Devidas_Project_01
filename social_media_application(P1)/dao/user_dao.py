from config.database import db
from models.user import User


class UserDAO:

    def find_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def find_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def create_user(self, username, email, password, role="user"):

        user = User(
            username=username,
            email=email,
            password=password,
            role=role
        )

        db.session.add(user)
        db.session.commit()

        return user