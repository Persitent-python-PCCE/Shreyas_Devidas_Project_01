from config.database import db
from models.post import Post


class PostDAO:

    def create_post(self, post):

        db.session.add(post)
        db.session.commit()

        return post


    def get_all_posts(self):

        return Post.query.order_by(
            Post.created_at.desc()
        ).all()


    def get_post_by_id(self, post_id):

        return Post.query.filter_by(
            id=post_id
        ).first()


    def update_post(self, post):

        try:
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            print("Update post error:", e)
            return False


    def delete_post(self, post):

        try:
            db.session.delete(post)
            db.session.commit()

            return True

        except Exception as e:
            db.session.rollback()

            print("Delete post error:", e)

            return False


    def get_posts_by_user(self, user_id):

        return Post.query.filter_by(
            user_id=user_id
        ).order_by(
            Post.created_at.desc()
        ).all()