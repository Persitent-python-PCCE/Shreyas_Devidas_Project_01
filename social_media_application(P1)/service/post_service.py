from dao.post_dao import PostDAO

class PostService:

    def __init__(self):

        self.post_dao = PostDAO()


    def create_post(self, user_id, content):

        if not content or not content.strip():
            return False, "Post content cannot be empty"

        post = self.post_dao.create_post(
            user_id,
            content
        )

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