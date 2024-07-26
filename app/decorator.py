from functools import wraps
from flask_jwt_extended import jwt_required


def auth_required(view_function):
    @wraps(view_function)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        return view_function(*args, **kwargs)
    return decorated_function