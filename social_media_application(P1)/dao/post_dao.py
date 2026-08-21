from config.database import db
from models.post import Post


class PostDAO:

    def create_post(self, user_id, content):

        post = Post(
            user_id=user_id,
            content=content
        )

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

        db.session.commit()


    def delete_post(self, post):

        db.session.delete(post)
        db.session.commit()