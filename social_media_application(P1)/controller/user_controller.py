from flask import Blueprint, render_template, request, redirect
from service.user_service import UserService

user_controller = Blueprint("user_controller", __name__)

user_service = UserService()
@user_controller.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form("username")
        email = request.form("email")
        password = request.form("password")

        user_service.register_user(username, email, password)

        return redirect("/users")

    return render_template("register.html")

@user_controller.route("/users")
def get_user():
    users = user_service.get_all_user()
    return render_template("user.html", users=users)

