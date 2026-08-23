from config.database import db
from models.like import Like


class LikeDAO:

    def create_like(self, post_id, user_id):

        like = Like(
            post_id=post_id,
            user_id=user_id
        )

        db.session.add(like)
        db.session.commit()

        return like


    def get_like(self, post_id, user_id):

        return Like.query.filter_by(
            post_id=post_id,
            user_id=user_id
        ).first()


    def delete_like(self, like):

        db.session.delete(like)
        db.session.commit()


    def get_likes_by_post(self, post_id):

        return Like.query.filter_by(
            post_id=post_id
        ).all()

    def count_likes(self):
        return Like.query.count()