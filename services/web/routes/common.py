from flask import Blueprint
from flask_login import login_required

from main import db
from models import User
from utils import has_permission

common_routes = Blueprint('common', __name__)


@common_routes.route("/")
@login_required
@has_permission('customer')
def hello_world():
    heroes = db.session.query(User).first()
    return "Hello"

