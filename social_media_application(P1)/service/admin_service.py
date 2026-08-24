from dao.admin_dao import AdminDAO


class AdminService:

    def __init__(self):
        self.admin_dao = AdminDAO()

    def get_dashboard_stats(self):

        return {
            "total_users": self.admin_dao.count_users(),
            "total_posts": self.admin_dao.count_posts(),
            "total_comments": self.admin_dao.count_comments(),
            "total_likes": self.admin_dao.count_likes(),
            "total_followers": self.admin_dao.count_followers()
        }