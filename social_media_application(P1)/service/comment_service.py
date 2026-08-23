from dao.comment_dao import CommentDAO
from dao.post_dao import PostDAO


class CommentService:

    def __init__(self):

        self.comment_dao = CommentDAO()
        self.post_dao = PostDAO()


    def add_comment(self, post_id, user_id, content):

        if not content or not content.strip():

            return False, "Comment cannot be empty"

        post = self.post_dao.get_post_by_id(post_id)

        if not post:

            return False, "Post not found"

        comment = self.comment_dao.create_comment(
            post_id,
            user_id,
            content
        )

        return True, comment


    def get_post_comments(self, post_id):

        post = self.post_dao.get_post_by_id(post_id)

        if not post:

            return False, "Post not found"

        comments = self.comment_dao.get_comments_by_post(
            post_id
        )

        return True, comments


    def delete_comment(self, comment_id, user_id):

        comment = self.comment_dao.get_comment_by_id(
            comment_id
        )

        if not comment:

            return False, "Comment not found"

        if comment.user_id != user_id:

            return False, "You can delete only your own comment"

        self.comment_dao.delete_comment(comment)

        return True, "Comment deleted successfully"


    def count_comments(self):
        return self.comment_dao.count_comments()