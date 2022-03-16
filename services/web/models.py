import enum

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Date, ForeignKey

from main import db


class Role(db.Model):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = Column(
        Integer,
        ForeignKey('roles.id', ondelete='CASCADE'),
        nullable=True,
        default=1
    )


class Category(db.Model):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)


class Analyses(db.Model):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    category_id = Column(
        Integer,
        ForeignKey('categories.id', ondelete='CASCADE'),
        nullable=True
    )


class OrderStatus(enum.Enum):
    in_progress = "in_progress"
    ready = "ready"


class CustomerAnalyses(db.Model):
    __tablename__ = "customer_analyses"

    id = Column(Integer, primary_key=True)
    analyse_id = Column(
        Integer,
        ForeignKey('analyses.id', ondelete='CASCADE'),
        nullable=True
    )
    customer_id = Column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE'),
        nullable=True
    )
    access = Column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE'),
        nullable=True
    )
    status = Column(
        db.Enum(OrderStatus),
        default=OrderStatus.in_progress,
    )
