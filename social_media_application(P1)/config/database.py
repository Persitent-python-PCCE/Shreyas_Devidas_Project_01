import os 

from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()

def init_db(app):
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    app.config["SQLALCHEMY_DATABASE_URI"] = (f"mysql+pymysql://{db_user}:{db_password}@localhost/social_media")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)