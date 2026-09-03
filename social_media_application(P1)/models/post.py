from config.database import db
from datetime import datetime


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),nullable=False)

    content = db.Column(db.Text, nullable=False)

    image = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    user = db.relationship(
        "User",
        backref="posts"
    )

    comments = db.relationship(
        "Comment",
        backref="post",
        cascade="all, delete-orphan",
        order_by="Comment.created_at.desc()"
    )

    likes = db.relationship(
        "Like",
        backref="post",
        cascade="all, delete-orphan"
    )