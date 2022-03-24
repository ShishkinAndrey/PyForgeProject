from flask import Blueprint, make_response, Response
from flask_login import login_required

from main import db
from models import Category, MedicalTest
from schema import medical_test_schema
from utils import has_permission


medical_tests = Blueprint('medical_tests', __name__)


@medical_tests.route('/', methods=['GET'])
@login_required
@has_permission(('customer',))
def get_medical_tests():
    all_analyses = db.session.query(MedicalTest).join(Category).with_entities(
        MedicalTest.id.label('medical_test_id'),
        MedicalTest.name.label('medical_test'),
        Category.name.label('category'),
        Category.id.label('category_id')
    ).all()

    return make_response({'data': [row._asdict() for row in all_analyses]}, 200)


@medical_tests.route('/<int:category_id>', methods=['GET'])
@login_required
@has_permission(('customer',))
def get_medical_tests_by_category(category_id):
    tests_by_category = db.session.query(MedicalTest).filter(MedicalTest.category_id == category_id).all()
    if not tests_by_category:
        return Response('Not found', status=404)
    return make_response({'data': [medical_test_schema.dump(row) for row in tests_by_category]}, 200)
