from marshmallow_sqlalchemy import auto_field, SQLAlchemyAutoSchema

from main import db
from models import MedicalTest, MedicalTestOrder, User


class MedicalTestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MedicalTest
        include_relationships = True
        load_instance = True
        sqla_session = db.session


medical_test_schema = MedicalTestSchema()


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        sqla_session = db.session

    role = auto_field()


user_schema = UserSchema()


class MedicalTestOrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MedicalTestOrder
        include_relationships = True
        load_instance = True
        sqla_session = db.session

    test = auto_field()
    customer = auto_field()
    access = auto_field()


medical_test_order_schema = MedicalTestOrderSchema()
