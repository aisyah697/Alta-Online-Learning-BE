from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer

class Mentees(db.Model):
    __tablename__ = "mentees"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    place_birth = db.Column(db.String(200))
    date_birth = db.Column(db.String(50))
    avatar = db.Column(db.String(255))
    background_education = db.Column(db.String(255))
    github = db.Column(db.String(255))
    description = db.Column(db.Text)
    salt = db.Column(db.String(200))
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    # altatest_history = db.relationship("AltatestHistories", cascade="all, delete-orphan", passive_deletes=True)
    # module_history = db.relationship("ModuleHistories", cascade="all, delete-orphan", passive_deletes=True)

    response_fields = {
        "id": fields.Integer,
        "username": fields.String,
        "full_name": fields.String,
        "email": fields.String,
        "address": fields.String,
        "phone": fields.String,
        "place_birth": fields.String,
        "date_birth": fields.String,
        "avatar": fields.String,
        "background_education": fields.String,
        "github": fields.String,
        "description": fields.String,
        "status": fields.String,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime
    }

    jwt_claims_fields = {
        "id": fields.Integer,
        "username": fields.String
    }

    def __init__ (self, username, password, full_name, email, address, phone, place_birth, date_birth, avatar, background_education, github, description, salt, status):
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
        self.address = address
        self.phone = phone
        self.place_birth = place_birth
        self.date_birth = date_birth
        self.avatar = avatar
        self.background_education = background_education
        self.github = github
        self.description = description
        self.salt = salt
        self.status = status

    def __rpr__(self):
        return "<Users %r>" % self.id