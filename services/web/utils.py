from functools import wraps

from flask import Response
from flask_login import current_user

from main import db
from models import Role


def has_permission(role):
    def login_by_role(func):
        @wraps(func)
        def role_validation(*args, **kwargs):
            current_user_role = db.session.query(Role).filter(Role.id == current_user.role).first().name
            if role != current_user_role:
                return Response('Permissions denied', status=403)
            else:
                return func(*args, **kwargs)
        return role_validation
    return login_by_role
