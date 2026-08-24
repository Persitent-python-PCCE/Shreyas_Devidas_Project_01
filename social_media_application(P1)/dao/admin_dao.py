from models.user import User
from models.post import Post
from models.comment import Comment
from models.like import Like
from models.follower import Follower


class AdminDAO:

    def count_users(self):
        return User.query.count()

    def count_posts(self):
        return Post.query.count()

    def count_comments(self):
        return Comment.query.count()

    def count_likes(self):
        return Like.query.count()

    def count_followers(self):
        return Follower.query.count()