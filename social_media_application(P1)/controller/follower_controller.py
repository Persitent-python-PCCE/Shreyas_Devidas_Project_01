from flask import Blueprint, request, jsonify

from service.follower_service import FollowerService
from utils.jwt_utils import user_required, get_current_user_id, get_current_user_role

follower_controller = Blueprint(
    "follower",
    __name__
)

follower_service = FollowerService()


# FOLLOW USER
@follower_controller.route(
    "/api/users/<int:following_id>/follow",
    methods=["POST"]
)
@user_required
def api_follow_user(following_id):

    follower_id = get_current_user_id()

    if int(follower_id) == following_id:
        return jsonify({
            "success": False,
            "message": "You cannot follow yourself"
        }), 400

    success, result = follower_service.follow_user(
        follower_id,
        following_id
    )

    if not success:
        return jsonify({
            "success": False,
            "message": result
        }), 400

    return jsonify({
        "success": True,
        "message": "User followed successfully"
    }), 201


# UNFOLLOW USER
@follower_controller.route(
    "/api/users/<int:following_id>/follow",
    methods=["DELETE"]
)
@user_required
def api_unfollow_user(following_id):

    follower_id = get_current_user_id()

    success, result = follower_service.unfollow_user(
        follower_id,
        following_id
    )

    if not success:
        return jsonify({
            "success": False,
            "message": result
        }), 400

    return jsonify({
        "success": True,
        "message": "User unfollowed successfully"
    }), 200


# GET FOLLOWERS
@follower_controller.route(
    "/api/users/<int:user_id>/followers",
    methods=["GET"]
)
def api_get_followers(user_id):

    followers = follower_service.get_followers(
        user_id
    )

    follower_list = []

    for follower in followers:

        follower_list.append({
            "id": follower.id,
            "follower_id": follower.follower_id,
            "following_id": follower.following_id
        })

    return jsonify({
        "success": True,
        "total_followers": len(follower_list),
        "followers": follower_list
    }), 200


# GET FOLLOWING
@follower_controller.route(
    "/api/users/<int:user_id>/following",
    methods=["GET"]
)
def api_get_following(user_id):

    following = follower_service.get_following(
        user_id
    )

    following_list = []

    for follow in following:

        following_list.append({
            "id": follow.id,
            "follower_id": follow.follower_id,
            "following_id": follow.following_id
        })

    return jsonify({
        "success": True,
        "total_following": len(following_list),
        "following": following_list
    }), 200