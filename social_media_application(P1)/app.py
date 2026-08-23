import os

from flask import Flask, render_template
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

from config.database import db, init_db

from models.user import User
from models.post import Post
from models.comment import Comment
from models.like import Like
from models.follower import Follower

from controller.auth_controller import auth_controller
from controller.post_controller import post_controller
from controller.comment_controller import comment_controller
from controller.like_controller import like_controller
from controller.follower_controller import follower_controller
from controller.admin_controller import admin_controller

from service.user_service import UserService

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)

init_db(app)

app.register_blueprint(auth_controller)
app.register_blueprint(post_controller)
app.register_blueprint(comment_controller)
app.register_blueprint(like_controller)
app.register_blueprint(follower_controller)
app.register_blueprint(admin_controller)


with app.app_context():
    db.create_all()
    user_service = UserService()
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    admin_role = os.getenv("ADMIN_ROLE")

    success, message = user_service.create_admin(
        admin_username,
        admin_email,
        admin_password,
        admin_role
    )
    print(message)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)