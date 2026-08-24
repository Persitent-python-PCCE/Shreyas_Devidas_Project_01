from flask import Blueprint, render_template, session, redirect, jsonify

from service.user_service import UserService
from service.post_service import PostService
from service.comment_service import CommentService
from service.like_service import LikeService

from service.admin_service import AdminService
from utils.jwt_utils import admin_required


admin_controller = Blueprint(
    "admin",
    __name__
)


admin_service = AdminService()

user_service = UserService()
post_service = PostService()
comment_service = CommentService()
like_service = LikeService()


@admin_controller.route("/admin/dashboard")
def admin_dashboard():

    if "user_id" not in session:
        return redirect("/login")

    user = user_service.get_user_by_id(
        session["user_id"]
    )

    if not user or user.role != "admin":
        return "Access denied", 403

    users = user_service.get_all_users()

    posts = post_service.get_all_posts()

    comments_count = comment_service.count_comments()
    likes_count = like_service.count_likes()

    return render_template(
        "admin_dashboard.html",

        users=users,

        users_count=len(users),

        posts_count=len(posts),

        comments_count=comments_count,

        likes_count=likes_count
    )


@admin_controller.route(
    "/api/admin/dashboard",
    methods=["GET"]
)
@admin_required
def api_admin_dashboard():

    stats = admin_service.get_dashboard_stats()

    return jsonify({
        "success": True,
        "message": "Admin dashboard data",
        "data": stats
    }), 200

@admin_controller.route(
    "/api/admin/users",
    methods=["GET"]
)
@admin_required
def get_all_users():

    users = user_service.get_all_users()

    user_list = []

    for user in users:

        user_list.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        })

    return jsonify({
        "success": True,
        "users": user_list
    }), 200