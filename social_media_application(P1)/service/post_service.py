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

        filename = None

        if image and image.filename:

            allowed_extensions = {
                "jpg",
                "jpeg",
                "png",
                "gif"
            }

            extension = image.filename.rsplit(".", 1)[-1].lower()

            if extension not in allowed_extensions:

                return False, "Invalid image type"

            # Create unique filename
            filename = secure_filename(
                str(uuid.uuid4()) + "." + extension
            )

            upload_folder = os.path.join(
                "static",
                "uploads"
            )

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            image.save(
                os.path.join(
                    upload_folder,
                    filename
                )
            )

        post = Post(
            user_id=user_id,
            content=content,
            image=filename
        )

        self.post_dao.create_post(post)

        return True, post


    def get_all_posts(self):

        return self.post_dao.get_all_posts()


    def update_post(self, post_id, user_id, content):

        post = self.post_dao.get_post_by_id(post_id)

        if not post:
            return False, "Post not found"

        if post.user_id != user_id:
            return False, "You can update only your own post"

        if not content or not content.strip():
            return False, "Post content cannot be empty"

        post.content = content

        self.post_dao.update_post(post)

        return True, post


    def delete_post(self, post_id, user_id):

        post = self.post_dao.get_post_by_id(post_id)

        if not post:
            return False, "Post not found"

        if post.user_id != user_id:
            return False, "You can delete only your own post"

        self.post_dao.delete_post(post)

        return True, "Post deleted successfully"