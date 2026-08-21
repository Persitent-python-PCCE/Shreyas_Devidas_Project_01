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