from flask.cli import FlaskGroup

from app import app
from main import db

from models import Role, Category, MedicalTest


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('add_roles')
def add_roles():
    db.session.add(Role(
        name="customer",
    ))
    db.session.add(Role(
        name="doctor",
    ))
    db.session.add(Role(
        name="assistant",
    ))
    db.session.commit()


@cli.command('add_data')
def add_default_data():
    db.session.add(Category(
        name="a",
    ))
    db.session.add(Category(
        name="b",
    ))
    db.session.add(Category(
        name="c",
    ))
    db.session.commit()

    db.session.add(MedicalTest(
        name="a",
        category_id=1
    ))
    db.session.add(MedicalTest(
        name="b",
        category_id=1
    ))
    db.session.add(MedicalTest(
        name="c",
        category_id=3
    ))
    db.session.add(MedicalTest(
        name="f",
        category_id=2
    ))
    db.session.add(MedicalTest(
        name="r",
        category_id=3
    ))
    db.session.commit()


if __name__ == "__main__":
    cli()
