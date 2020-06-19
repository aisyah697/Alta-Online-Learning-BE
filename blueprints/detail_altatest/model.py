from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer

from blueprints.question_altatest.model import QuestionsAltatest
from blueprints.altatest.model import Altatests


class DetailsAltatest(db.Model):
    __tablename__ = "details_altatest"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    altatest_id = db.Column(db.Integer, db.ForeignKey(Altatests.id, ondelete="CASCADE"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(QuestionsAltatest.id, ondelete="CASCADE"), nullable=False)
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "altatest_id": fields.Integer,
        "question_id": fields.Integer,
        "status": fields.Boolean,
        "created_at": fields.DateTime,
        "updated_at": fields.DateTime
    }

    def __init__ (self, altatest_id, question_id,status):
        self.altatest_id = altatest_id
        self.question_id = question_id
        self.status = status

    def __rpr__(self):
        return "<Users %r>" % self.id