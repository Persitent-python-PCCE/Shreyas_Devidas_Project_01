from config.database import db
from models.comment import Comment


class CommentDAO:

    def create_comment(self, post_id, user_id, content):

        comment = Comment(
            post_id=post_id,
            user_id=user_id,
            content=content
        )

        db.session.add(comment)
        db.session.commit()

        return comment


    def get_comments_by_post(self, post_id):

        return Comment.query.filter_by(
            post_id=post_id
        ).order_by(
            Comment.created_at.desc()
        ).all()


    def get_comment_by_id(self, comment_id):

        return Comment.query.get(comment_id)


    def delete_comment(self, comment):

        db.session.delete(comment)
        db.session.commit()