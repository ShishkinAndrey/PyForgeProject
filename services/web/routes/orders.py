import os

from flask import Blueprint, make_response, render_template, request, Response, send_from_directory
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from config import UPLOAD_FOLDER
from main import db
from models import MedicalTestOrder, OrderStatus, Role, User
from schema import medical_test_order_schema
from utils import allowed_file, has_permission


orders = Blueprint('orders', __name__)


@orders.route('/', methods=['GET'])
@login_required
@has_permission(('doctor',))
def get_available_orders():
    all_orders = db.session.query(MedicalTestOrder).filter(MedicalTestOrder.access == current_user.id).all()

    return make_response({'data': [medical_test_order_schema.dump(row) for row in all_orders]}, 200)


@orders.route('/<int:order_id>', methods=['GET'])
@login_required
@has_permission(('doctor',))
def get_available_order(order_id):
    order = db.session.query(MedicalTestOrder).filter(
        MedicalTestOrder.id == order_id,
        MedicalTestOrder.access == current_user.id
    ).first()
    if not order:
        return Response('Not found', status=404)
    return make_response(medical_test_order_schema.dump(order), 200)


@orders.route('/', methods=['POST'])
@login_required
@has_permission(('customer',))
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


@orders.route('/<int:order_id>/access', methods=['PATCH'])
@login_required
@has_permission(('customer',))
def add_access(order_id):
    order = db.session.query(MedicalTestOrder).filter(MedicalTestOrder.id == order_id).first()
    if not order:
        return Response('Not found', status=404)

    order.access = request.json['access']
    db.session.commit()

    return Response('Access for test is added', status=200)


@orders.route('/<int:order_id>/result', methods=['GET', 'POST'])
@login_required
@has_permission(('assistant',))
def add_result(order_id):
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            return Response('Bad request', status=400)
        order = db.session.query(MedicalTestOrder).filter(MedicalTestOrder.id == order_id).first()
        if not order:
            return Response('Not found', status=404)
        if file and allowed_file(file.filename):
            order = db.session.query(MedicalTestOrder).filter(MedicalTestOrder.id == order_id).first()
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            order.result = filename
            order.status = OrderStatus.ready
            db.session.commit()
            return Response('Result is added', status=200)
    return render_template('add_file.html')


@orders.route('/result/<name>', methods=['GET'])
@login_required
@has_permission(('customer', 'doctor'))
def get_file(name):
    return send_from_directory(UPLOAD_FOLDER, name, as_attachment=True)
