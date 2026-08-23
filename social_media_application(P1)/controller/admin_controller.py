from flask import Blueprint, jsonify

from service.user_service import UserService
from utils.jwt_utils import admin_required


admin_controller = Blueprint(
    "admin",
    __name__
)

user_service = UserService()


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