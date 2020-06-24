from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer

from blueprints.exam.model import Exams


class Livecodes(db.Model):
    __tablename__ = "livecodes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exam_id = db.Column(db.Integer, db.ForeignKey(Exams.id, ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(250))
    description = db.Column(db.Text)
    link = db.Column(db.String(250))
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "exam_id": fields.Integer,
        "name": fields.String,
        "description": fields.String,
        "link": fields.String,
        "status": fields.Boolean,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime,
    }

    def __init__(self, exam_id, name, description, link, status):
        self.exam_id = exam_id
        self.name = name
        self.description = description
        self.link = link
        self.status = status

    def __rpr__(self):
        return "<Questions %r>" % self.id