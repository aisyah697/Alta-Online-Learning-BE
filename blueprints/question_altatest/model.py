from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer

from blueprints.admin.model import Admins


class QuestionsAltatest(db.Model):
    __tablename__ = "questions_altatest"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey(Admins.id, ondelete="CASCADE"), nullable=False)
    question = db.Column(db.Text, nullable=False)
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    choices_altatest = db.relationship("ChoicesAltatest", cascade="all, delete-orphan", passive_deletes=True)

    response_fields = {
        "id": fields.Integer,
        "admin_id": fields.Integer,
        "question": fields.String,
        "status": fields.Boolean,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime,
    }

    def __init__(self, admin_id, question, status):
        self.admin_id = admin_id
        self.question = question
        self.status = status

    def __rpr__(self):
        return "<Questions %r>" % self.id