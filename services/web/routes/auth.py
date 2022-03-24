from flask import Blueprint, request, Response
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from main import db
from models import User
from schema import user_schema


auth_routes = Blueprint('auth_routes', __name__)


@auth_routes.route('/signup', methods=['POST'])
def signup():
    data = {
        'email': request.json['email'],
        'password': generate_password_hash(request.json['password'], method='sha256'),
        'first_name': request.json['first_name'],
        'last_name': request.json['last_name'],
        'role': request.json['role']
    }
    new_user = user_schema.load(data)

    user = User.query.filter_by(email=request.json.get('email')).first()

    if user:
        return Response('User already exists', status=400)

    db.session.add(new_user)
    db.session.commit()

    return Response('Successfully sign up', status=200)


@auth_routes.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return Response('Incorrect email or password', status=400)

    login_user(user)
    return Response('Successfully logged in', status=200)


@auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return Response('Successfully logged out', status=200)
