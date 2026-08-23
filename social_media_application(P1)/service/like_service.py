from dao.like_dao import LikeDAO
from dao.post_dao import PostDAO


class LikeService:

    def __init__(self):

        self.like_dao = LikeDAO()
        self.post_dao = PostDAO()


    def like_post(self, post_id, user_id):

        post = self.post_dao.get_post_by_id(post_id)

        if not post:

            return False, "Post not found"

        existing_like = self.like_dao.get_like(
            post_id,
            user_id
        )

        if existing_like:

            return False, "Post already liked"

        like = self.like_dao.create_like(
            post_id,
            user_id
        )

        return True, like


    def unlike_post(self, post_id, user_id):

        like = self.like_dao.get_like(
            post_id,
            user_id
        )

        if not like:

            return False, "Post is not liked"

        self.like_dao.delete_like(like)

        return True, "Post unliked successfully"


    def get_post_likes(self, post_id):

        post = self.post_dao.get_post_by_id(post_id)

        if not post:

            return False, "Post not found"

        likes = self.like_dao.get_likes_by_post(
            post_id
        )

        return True, likes