from flask import Blueprint, request, Response, jsonify
from flask_login import login_required, current_user

from main import db
from models import MedicalTest, Category, OrderStatus, User, Role, MedicalTestOrder
from schema import medical_test_order_schema
from utils import has_permission


orders = Blueprint('orders', __name__)


@orders.route("/", methods=['GET'])
@login_required
@has_permission('doctor')
def get_available_orders():
    all_orders = db.session.query(MedicalTestOrder).filter(MedicalTestOrder.access == current_user.id).all()

    return Response({'data': [medical_test_order_schema.dump(row) for row in all_orders]}, status=200)


@orders.route("/<int:order_id>", methods=['GET'])
@login_required
@has_permission('doctor')
def get_available_order(order_id):
    order = db.session.query(MedicalTestOrder).filter(
        MedicalTestOrder.id == order_id,
        MedicalTestOrder.access == current_user.id
    ).first()

    return Response(medical_test_order_schema.dump(order), status=200)


@orders.route("/", methods=['POST'])
@login_required
@has_permission('customer')
def make_an_order():
    if request.json.get('access'):
        access = db.session.query(User).join(Role).filter(
            User.id == request.json.get('access'),
            Role.name == 'doctor').first()
        if not access:
            return Response('Not found', status=404)
    data = {
        'test': request.json.get('test'),
        'customer': current_user.id,
        'status': OrderStatus.created,
        'access': request.json.get('access')
    }

    order = medical_test_order_schema.load(data)

    db.session.add(order)
    db.session.commit()

    return Response('Order is created', status=200)
