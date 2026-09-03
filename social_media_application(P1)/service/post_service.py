import os
import uuid

from werkzeug.utils import secure_filename

from config.database import db
from models.post import Post
from dao.post_dao import PostDAO

class PostService:

    def __init__(self):

        self.post_dao = PostDAO()


    def create_post(self, user_id, content, image=None):

        if not content or not content.strip():
            return False, "Post content is required"

        post = Post(
            user_id=user_id,
            content=content,
            image=image
        )

        self.post_dao.create_post(post)

        return True, post


    def get_all_posts(self, current_user_id=None):

        posts = self.post_dao.get_all_posts()

        for post in posts:

            post.like_count = len(post.likes)

            post.comment_count = len(post.comments)

            post.is_liked = False

            if current_user_id:

                for like in post.likes:

                    if str(like.user_id) == str(current_user_id):

                        post.is_liked = True

                        break

        return posts


    def update_post(self, post_id, user_id, content, image_path):

        post = self.post_dao.get_post_by_id(post_id)

        if not post:
            return False, "Post not found"

        if str(post.user_id) != str(user_id):
            return False, "You are not allowed to update this post"

        post.content = content
        post.image = image_path

        success = self.post_dao.update_post(post)

        if not success:
            return False, "Failed to update post"

        return True, post


    def delete_post(self, post_id, user_id):

        post = self.post_dao.get_post_by_id(post_id)

        if not post:
            return False, "Post not found"

        if str(post.user_id) != str(user_id):
            return False, "You are not allowed to delete this post"

        success = self.post_dao.delete_post(post)

        if not success:
            return False, "Failed to delete post"

        return True, "Post deleted successfully"


    def get_posts_by_user(self, user_id):

        return self.post_dao.get_posts_by_user(user_id)

    def get_followers_count(self, user_id):

        return self.follower_dao.get_followers_count(user_id)


    def get_following_count(self, user_id):

        return self.follower_dao.get_following_count(user_id)