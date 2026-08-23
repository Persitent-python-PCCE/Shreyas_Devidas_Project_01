from functools import wraps

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity


def user_required(func):

    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):

    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):

        claims = get_jwt()

        role = claims.get("role")
        
        if role != "admin":
            return jsonify({
                "success": False,
                "message": "Admin access required"
            }), 403

        return func(*args, **kwargs)

    return wrapper


def get_current_user_id():

    return get_jwt_identity()


def get_current_user_role():

    claims = get_jwt()

    return claims.get("role")