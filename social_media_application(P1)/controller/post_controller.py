import os
import uuid
from flask import Blueprint, render_template, request, redirect, session, jsonify

from service.post_service import PostService

from werkzeug.utils import secure_filename

from service.post_service import PostService

post_controller = Blueprint(
    "post",
    __name__
)

post_service = PostService()


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

        user_id = session.get("user_id")

        success, result = post_service.create_post(
            user_id,
            content
        )

        if not success:

            return render_template(
                "create_post.html",
                error=result
            )

        return redirect("/feed")

    return render_template("create_post.html")



@post_controller.route("/api/posts", methods=["POST"])
def api_create_post():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    user_id = data.get("user_id")
    content = data.get("content")

    if not user_id:
        return jsonify({
            "success": False,
            "message": "User ID is required"
        }), 400

    if not content or not content.strip():
        return jsonify({
            "success": False,
            "message": "Post content is required"
        }), 400

    success, result = post_service.create_post(
        user_id,
        content
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
def api_update_post(post_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    user_id = data.get("user_id")
    content = data.get("content")

    if not user_id:
        return jsonify({
            "success": False,
            "message": "User ID is required"
        }), 400

    if not content or not content.strip():
        return jsonify({
            "success": False,
            "message": "Post content is required"
        }), 400

    success, result = post_service.update_post(
        post_id,
        user_id,
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
            "created_at": str(result.created_at)
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

@post_controller.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_apipost(post_id):

    user_id = request.json.get("user_id")

    if not user_id:
        return jsonify({
            "message": "user_id is required"
        }), 400

    success, message = post_service.delete_post(
        post_id,
        user_id
    )

    if not success:
        return jsonify({
            "message": message
        }), 404

    return jsonify({
        "message": message
    }), 200