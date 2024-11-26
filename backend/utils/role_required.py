from functools import wraps
from flask_jwt_extended import get_jwt_identity
from application.models import User,Professional


def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                current_user_email = get_jwt_identity()
                user = User.query.filter_by(email = current_user_email).first()
                if user and user.role == required_role:
                    return fn(*args , **kwargs)
                else:
                    return {'message' : 'Access Denied'} , 401
            except Exception as e:
                return {'message' : 'Internal Server Error'} , 500
        return wrapper
    return decorator