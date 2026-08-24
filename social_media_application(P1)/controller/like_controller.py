from flask import Blueprint, request, jsonify

from service.like_service import LikeService
from utils.jwt_utils import user_required, get_current_user_id, get_current_user_role

like_controller = Blueprint("like", __name__)

like_service = LikeService()

@like_controller.route("/api/posts/<int:post_id>/like", methods=["POST"])
@user_required
def api_like_post(post_id):

    user_id = get_current_user_id()

    success, result = like_service.like_post(
        post_id,
        user_id
    )

    if not success:

        return jsonify({
            "success": False,
            "message": result
        }), 400

    return jsonify({
        "success": True,
        "message": "Post liked successfully"
    }), 201


@like_controller.route("/api/posts/<int:post_id>/like", methods=["DELETE"])
@user_required
def api_unlike_post(post_id):

    user_id = get_current_user_id()

    success, result = like_service.unlike_post(
        post_id,
        user_id
    )

    if not success:

        return jsonify({
            "success": False,
            "message": result
        }), 400

    return jsonify({
        "success": True,
        "message": "Post unliked successfully"
    }), 200



@like_controller.route( "/api/posts/<int:post_id>/likes", methods=["GET"])
def api_get_likes(post_id):

    success, result = like_service.get_post_likes(
        post_id
    )

    if not success:
        return jsonify({
            "success": False,
            "message": result
        }), 404

    like_list = []

    for like in result:

        like_list.append({
            "id": like.id,
            "post_id": like.post_id,
            "user_id": like.user_id
        })

    return jsonify({
        "success": True,
        "total_likes": len(like_list),
        "likes": like_list
    }), 200