import os
import uuid
from flask import Blueprint, render_template, request, redirect, session, jsonify

from service.post_service import PostService
from utils.jwt_utils import user_required, get_current_user_id, get_current_user_role
from werkzeug.utils import secure_filename
from flask import current_app

from service.post_service import PostService

post_controller = Blueprint(
    "post",
    __name__
)

post_service = PostService()

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )

UPLOAD_FOLDER = "static/uploads/posts"

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "gif",
    "webp"
}

MAX_FILE_SIZE = 5 * 1024 * 1024   

@post_controller.route("/feed", methods=["GET", "POST"])
def feed():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        content = request.form.get("content")
        user_id = session.get("user_id")

        success, result = post_service.create_post(
            user_id,
            content
        )

        if not success:

            posts = post_service.get_all_posts()

            return render_template(
                "feed.html",
                posts=posts,
                error=result
            )

    posts = post_service.get_all_posts()

    return render_template(
        "feed.html",
        posts=posts
    )

@post_controller.route("/api/posts", methods=["GET"])
def api_get_posts():

    posts = post_service.get_all_posts()

    post_list = []

    for post in posts:

        post_list.append({
            "id": post.id,
            "user_id": post.user_id,
            "content": post.content,
            "image": post.image,
            "created_at": str(post.created_at)
        })

    return jsonify({
        "success": True,
        "posts": post_list
    }), 200




@post_controller.route("/create-post", methods=["GET", "POST"])
def create_post():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        content = request.form.get("content")

        image = request.files.get("image")

        user_id = session.get("user_id")

        success, result = post_service.create_post(
            user_id,
            content,
            image
        )

        if not success:

            return render_template(
                "create_post.html",
                error=result
            )

        return redirect("/feed")

    return render_template("create_post.html")




@post_controller.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):

    if "user_id" not in session:
        return redirect("/login")

    user_id = session.get("user_id")

    post = post_service.post_dao.get_post_by_id(post_id)

    if not post:
        return "Post not found", 404

    if post.user_id != user_id:
        return "You cannot edit this post", 403


    if request.method == "POST":

        content = request.form.get("content")

        success, result = post_service.update_post(
            post_id,
            user_id,
            content
        )

        if not success:

            return render_template(
                "edit_post.html",
                post=post,
                error=result
            )

        return redirect("/feed")


    return render_template(
        "edit_post.html",
        post=post
    )


@post_controller.route("/api/posts/<int:post_id>", methods=["PUT"])
@user_required
def api_update_post(post_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    content = data.get("content")

    if not content:
        return jsonify({
            "success": False,
            "message": "Content is required"
        }), 400

    user_id = get_current_user_id()
    role = get_current_user_role()

    post = post_service.post_dao.get_post_by_id(post_id)

    if not post:

        return jsonify({
            "success": False,
            "message": "Post not found"
        }), 404

    # Normal user can edit only own post
    if role != "admin" and post.user_id != int(user_id):

        return jsonify({
            "success": False,
            "message": "You can edit only your own post"
        }), 403

    success, result = post_service.update_post(
        post_id,
        post.user_id,
        content
    )

    if not success:

        return jsonify({
            "success": False,
            "message": result
        }), 400

    return jsonify({
        "success": True,
        "message": "Post updated successfully",
        "post": {
            "id": result.id,
            "user_id": result.user_id,
            "content": result.content,
            "image": result.image,
            "created_at": str(result.created_at),
            "updated_at": str(result.updated_at)
        }
    }), 200

@post_controller.route("/delete-post/<int:post_id>", methods=["POST"])
def delete_post(post_id):

    if "user_id" not in session:
        return redirect("/login")

    user_id = session.get("user_id")

    success, message = post_service.delete_post(
        post_id,
        user_id
    )

    if not success:
        return message, 403

    return redirect("/feed")

@post_controller.route(
    "/api/posts/<int:post_id>",
    methods=["DELETE"]
)
@user_required
def api_delete_post(post_id):

    user_id = get_current_user_id()
    role = get_current_user_role()

    post = post_service.post_dao.get_post_by_id(post_id)

    if not post:

        return jsonify({
            "success": False,
            "message": "Post not found"
        }), 404

    
    if role != "admin" and post.user_id != int(user_id):

        return jsonify({
            "success": False,
            "message": "You can delete only your own post"
        }), 403

    success, message = post_service.delete_post(
        post_id,
        post.user_id
    )

    if not success:

        return jsonify({
            "success": False,
            "message": message
        }), 400

    return jsonify({
        "success": True,
        "message": "Post deleted successfully"
    }), 200


@post_controller.route("/api/posts", methods=["POST"])
def api_create_post():

    user_id = request.form.get("user_id")
    content = request.form.get("content")

    # Check user id
    if not user_id:
        return jsonify({
            "success": False,
            "message": "User ID is required"
        }), 400

    # Check content
    if not content or not content.strip():
        return jsonify({
            "success": False,
            "message": "Post content is required"
        }), 400

    image_path = None

    # Image is optional
    if "image" in request.files:

        image = request.files["image"]

        # Check image name
        if image.filename == "":
            return jsonify({
                "success": False,
                "message": "No image selected"
            }), 400

        # Check extension
        if not allowed_file(image.filename):
            return jsonify({
                "success": False,
                "message": "Invalid image type"
            }), 400

        # Check file size
        image.seek(0, os.SEEK_END)

        file_size = image.tell()

        image.seek(0)

        if file_size > MAX_FILE_SIZE:
            return jsonify({
                "success": False,
                "message": "Image size must be less than 5 MB"
            }), 400

        # Create unique filename
        original_filename = secure_filename(image.filename)

        extension = original_filename.rsplit(".", 1)[1].lower()

        filename = str(uuid.uuid4()) + "." + extension

        # Create upload folder
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # Full file path
        file_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        # Save image
        image.save(file_path)

        # Path stored in database
        image_path = "uploads/posts/" + filename

    # Create post
    success, result = post_service.create_post(
        user_id,
        content,
        image_path
    )

    if not success:

        return jsonify({
            "success": False,
            "message": result
        }), 400

    return jsonify({
        "success": True,
        "message": "Post created successfully",
        "post": {
            "id": result.id,
            "user_id": result.user_id,
            "content": result.content,
            "image": result.image,
            "created_at": str(result.created_at)
        }
    }), 201


