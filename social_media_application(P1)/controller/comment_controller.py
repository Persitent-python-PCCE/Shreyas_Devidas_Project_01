from flask import Blueprint, request, jsonify

from service.comment_service import CommentService
from utils.jwt_utils import user_required, get_current_user_id, get_current_user_role

comment_controller = Blueprint(
    "comment",
    __name__
)

comment_service = CommentService()


# CREATE COMMENT
@comment_controller.route(
    "/api/posts/<int:post_id>/comments",
    methods=["POST"]
)
@user_required
def api_create_comment(post_id):

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
            "message": "Comment content is required"
        }), 400

    user_id = get_current_user_id()

    success, result = comment_service.create_comment(
        user_id,
        post_id,
        content
    )

    if not success:
        return jsonify({
            "success": False,
            "message": result
        }), 400

    return jsonify({
        "success": True,
        "message": "Comment added successfully",
        "comment": {
            "id": result.id,
            "user_id": result.user_id,
            "post_id": result.post_id,
            "content": result.content,
            "created_at": str(result.created_at)
        }
    }), 201

# GET COMMENTS
@comment_controller.route(
    "/api/posts/<int:post_id>/comments",
    methods=["GET"]
)
def api_get_comments(post_id):

    success, result = comment_service.get_post_comments(
        post_id
    )

    if not success:
        return jsonify({
            "success": False,
            "message": result
        }), 404

    comment_list = []

    for comment in result:

        comment_list.append({
            "id": comment.id,
            "post_id": comment.post_id,
            "user_id": comment.user_id,
            "content": comment.content,
            "created_at": str(comment.created_at)
        })

    return jsonify({
        "success": True,
        "comments": comment_list
    }), 200


# DELETE COMMENT
@comment_controller.route(
    "/api/comments/<int:comment_id>",
    methods=["DELETE"]
)
@user_required
def api_delete_comment(comment_id):

    user_id = get_current_user_id()
    role = get_current_user_role()

    comment = comment_service.comment_dao.get_comment_by_id(
        comment_id
    )

    if not comment:

        return jsonify({
            "success": False,
            "message": "Comment not found"
        }), 404

    # Normal user → only own comment
    if role != "admin" and comment.user_id != int(user_id):

        return jsonify({
            "success": False,
            "message": "You can delete only your own comment"
        }), 403

    success, message = comment_service.delete_comment(
        comment_id
    )

    if not success:

        return jsonify({
            "success": False,
            "message": message
        }), 400

    return jsonify({
        "success": True,
        "message": "Comment deleted successfully"
    }), 200