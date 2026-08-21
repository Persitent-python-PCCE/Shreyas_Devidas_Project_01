import os

from flask import Flask, render_template
from dotenv import load_dotenv

from config.database import db, init_db

from models.user import User
from models.post import Post
from models.comment import Comment
from models.like import Like
from models.follower import Follower

from controller.auth_controller import auth_controller
from controller.post_controller import post_controller

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

init_db(app)

app.register_blueprint(auth_controller)
app.register_blueprint(post_controller)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)