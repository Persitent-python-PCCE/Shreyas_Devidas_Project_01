from config.database import db
from datetime import datetime


class Follower(db.Model):
    __tablename__ = "followers"

    id = db.Column(db.Integer, primary_key=True)

    follower_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    following_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    __table_args__ = (
        db.UniqueConstraint(
            "follower_id",
            "following_id",
            name="unique_follow"
        ),
    )