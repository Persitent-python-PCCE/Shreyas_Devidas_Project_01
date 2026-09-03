from config.database import db
from models.follower import Follower


class FollowerDAO:

    def create_follow(self, follower_id, following_id):

        follow = Follower(
            follower_id=follower_id,
            following_id=following_id
        )

        db.session.add(follow)
        db.session.commit()

        return follow


    def get_follow(self, follower_id, following_id):

        return Follower.query.filter_by(
            follower_id=follower_id,
            following_id=following_id
        ).first()


    def delete_follow(self, follow):

        db.session.delete(follow)
        db.session.commit()


    def get_followers(self, user_id):

        return Follower.query.filter_by(
            following_id=user_id
        ).all()


    def get_following(self, user_id):

        return Follower.query.filter_by(
            follower_id=user_id
        ).all()

    def get_followers_count(self, user_id):

        return Follower.query.filter_by(
            following_id=user_id
        ).count()

    def get_following_count(self, user_id):

        return Follower.query.filter_by(
            follower_id=user_id
        ).count()