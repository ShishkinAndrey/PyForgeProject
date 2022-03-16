from flask import Blueprint, jsonify
from flask_login import login_required

from main import db
from models import MedicalTest, Category
from schema import medical_test_schema
from utils import has_permission


medical_tests = Blueprint('medical_tests', __name__)


@medical_tests.route("/", methods=['GET'])
@login_required
@has_permission('customer')
def get_medical_tests():
    all_analyses = db.session.query(MedicalTest).join(Category).with_entities(
        MedicalTest.id.label('medical_test_id'),
        MedicalTest.name.label('medical_test'),
        Category.name.label('category'),
        Category.id.label('category_id')
    ).all()

    return {'data': [row._asdict() for row in all_analyses]}


@medical_tests.route("/<int:category_id>", methods=['GET'])
@login_required
@has_permission('customer')
def get_medical_tests_by_category(category_id):
    all_analyses = db.session.query(MedicalTest).filter(MedicalTest.category_id==category_id).all()

    return {'data': [medical_test_schema.dump(row) for row in all_analyses]}


@medical_tests.route("/", methods=['POST'])
@login_required
@has_permission('customer')
def make_an_order():
    pass