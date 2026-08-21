from flask import Blueprint, render_template, request, redirect, session, jsonify
from service.user_service import UserService


auth_controller = Blueprint("auth", __name__)

user_service = UserService()


@auth_controller.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        success, message = user_service.register_user(
            username,
            email,
            password
        )

        if not success:

            return render_template(
                "register.html",
                error=message
            )

        return redirect("/login")

    return render_template("register.html")


@auth_controller.route("/api/register", methods = ["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    success, message = user_service.register_user(username, email, password)
    if not success:
        return jsonify({
            "success": False,
            "message": message
        }), 400
    return jsonify({
        "success": True,
        "message": message
    }), 201



@auth_controller.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        success, result = user_service.login_user(
            email,
            password
        )

        if not success:

            return render_template(
                "login.html",
                error=result
            )

        user = result

        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role

        return redirect("/feed")


    return render_template("login.html")


@auth_controller.route("/logout")
def logout():

    session.clear()

    return redirect("/")