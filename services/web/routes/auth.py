from flask import Blueprint, redirect, url_for, request, Response
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from main import db
from models import User


auth_routes = Blueprint('auth_routes', __name__)


@auth_routes.route('/signup', methods=['POST'])
def signup_post():
    email = request.json['email']
    password = request.json['password']
    first_name = request.json['first_name']
    last_name = request.json['last_name']

    user = User.query.filter_by(email=request.json.get('email')).first()

    if user:
        return Response("User already exists", status=400)

    new_user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=generate_password_hash(password, method='sha256'),
    )
    db.session.add(new_user)
    db.session.commit()

    return Response("Successfully signed in", status=200)


@auth_routes.route('/login', methods=['POST'])
def login_post():
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return Response("Incorrect email or password", status=400)

    login_user(user)
    return Response("Successfully logged in", status=200)


@auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return Response("Successfully logged out", status=200)
