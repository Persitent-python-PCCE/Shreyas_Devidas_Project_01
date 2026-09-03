from flask import Blueprint, render_template, request, redirect, session, jsonify
from service.user_service import UserService
from service.post_service import PostService
from service.follower_service import FollowerService
from flask_jwt_extended import create_access_token
from utils.jwt_utils import user_required, get_current_user_id

auth_controller = Blueprint("auth", __name__)

user_service = UserService()
post_service = PostService()
follower_service = FollowerService()


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
def api_register():
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


@auth_controller.route(
    "/api/forgot-password",
    methods=["POST"]
)
def api_forgot_password():

    data = request.get_json()

    email = data.get("email")

    if not email:

        return jsonify({
            "success": False,
            "message": "Email is required"
        }), 400

    success, result = user_service.forgot_password(email)

    return jsonify({
        "success": success,
        "message": "If the email exists, a reset link has been generated.",
        "reset_token": result
    }), 200

@auth_controller.route(
    "/api/reset-password",
    methods=["POST"]
)
def api_reset_password():

    data = request.get_json()

    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:

        return jsonify({
            "success": False,
            "message": "Token and new password are required"
        }), 400

    success, message = user_service.reset_password(
        token,
        new_password
    )

    if not success:

        return jsonify({
            "success": False,
            "message": message
        }), 400

    return jsonify({
        "success": True,
        "message": message
    }), 200

@auth_controller.route("/api/profile", methods=["GET"])
@user_required
def api_get_profile():

    user_id = get_current_user_id()

    user = user_service.get_user_by_id(
        int(user_id)
    )

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    return jsonify({
        "success": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
        }
    }), 200

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

        if user.role == "admin":
            return redirect("/admin/dashboard")

        return redirect("/feed")



    return render_template("login.html")


@auth_controller.route("/api/login", methods=["POST"])
def api_login():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    success, result = user_service.login_user(
        email,
        password
    )

    if not success:
        return jsonify({
            "success": False,
            "message": result
        }), 401

    user = result

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )

    return jsonify({
        "success": True,
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }), 200





@auth_controller.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@auth_controller.route("/api/logout", methods=["POST"])
def api_logout():

    session.clear()

    return jsonify({
        "success": True,
        "message": "Logout successful"
    }), 200

@auth_controller.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session.get("user_id")

    user = user_service.get_user_by_id(user_id)

    if not user:
        return "User not found", 404

    posts = post_service.get_posts_by_user(user_id)

    followers_count = follower_service.get_followers(
        user_id
    )

    following_count = follower_service.get_following(
        user_id
    )

    return render_template(
        "profile.html",
        user=user,
        posts=posts,
        followers_count=followers_count,
        following_count=following_count
    )