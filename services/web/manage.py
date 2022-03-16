from flask.cli import FlaskGroup

from app import app
from main import db

from models import Role


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
        name="asistant",
    ))
    db.session.commit()


if __name__ == "__main__":
    cli()
