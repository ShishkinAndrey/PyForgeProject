from flask.cli import FlaskGroup

from app import app
from main import db
from models import Category, MedicalTest, Role


cli = FlaskGroup(app)


@cli.command('create_db')
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('add_roles')
def add_roles():
    db.session.add(Role(
        name='customer',
    ))
    db.session.add(Role(
        name='doctor',
    ))
    db.session.add(Role(
        name='assistant',
    ))
    db.session.commit()


@cli.command('add_data')
def add_default_data():
    db.session.add(Category(
        name='Blood Disorder tests',
    ))
    db.session.add(Category(
        name='Diabetes tests',
    ))
    db.session.add(Category(
        name='Immunity Tests',
    ))
    db.session.commit()

    db.session.add(MedicalTest(
        name='Antibodies Screen Blood Test',
        category_id=1
    ))
    db.session.add(MedicalTest(
        name='D-Dimer Blood Test',
        category_id=1
    ))
    db.session.add(MedicalTest(
        name='Vitamin K1 Blood Test',
        category_id=1
    ))
    db.session.add(MedicalTest(
        name='Insulin Fasting Blood Test',
        category_id=2
    ))
    db.session.add(MedicalTest(
        name='Glucose Serum Test',
        category_id=2
    ))
    db.session.add(MedicalTest(
        name='C-Peptide Serum Test',
        category_id=2
    ))
    db.session.add(MedicalTest(
        name='Immunity Blood Test Panel',
        category_id=3
    ))
    db.session.add(MedicalTest(
        name='Antibodies Screen Blood Test',
        category_id=3
    ))
    db.session.commit()


if __name__ == '__main__':
    cli()
