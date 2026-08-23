from dao.follower_dao import FollowerDAO
from dao.user_dao import UserDAO


class FollowerService:

    def __init__(self):

        self.follower_dao = FollowerDAO()
        self.user_dao = UserDAO()


    def follow_user(self, follower_id, following_id):

        if follower_id == following_id:

            return False, "You cannot follow yourself"

        user = self.user_dao.get_user_by_id(
            following_id
        )

        if not user:

            return False, "User not found"

        existing_follow = self.follower_dao.get_follow(
            follower_id,
            following_id
        )

        if existing_follow:

            return False, "Already following this user"

        follow = self.follower_dao.create_follow(
            follower_id,
            following_id
        )

        return True, follow


    def unfollow_user(self, follower_id, following_id):

        follow = self.follower_dao.get_follow(
            follower_id,
            following_id
        )

        if not follow:

            return False, "You are not following this user"

        self.follower_dao.delete_follow(follow)

        return True, "Unfollowed successfully"


    def get_followers(self, user_id):

        return self.follower_dao.get_followers(user_id)


    def get_following(self, user_id):

        return self.follower_dao.get_following(user_id)