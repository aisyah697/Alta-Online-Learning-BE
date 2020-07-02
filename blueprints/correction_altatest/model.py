from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer

from blueprints.history_altatest.model import HistoriesAltatest


class CorrectionsAltatest(db.Model):
    __tablename__ = "corrections_altatest"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    history_altatest_id = db.Column(db.Integer, db.ForeignKey(HistoriesAltatest.id, ondelete="CASCADE"), nullable=False)
    question_altatest_id = db.Column(db.Integer)
    answer_id = db.Column(db.Integer)
    is_correct = db.Column(db.Boolean)
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "history_altatest_id": fields.Integer,
        "question_altatest_id": fields.Integer,
        "answer_id": fields.Integer,
        "is_correct": fields.Boolean,
        "status": fields.Boolean,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime,
    }

    def __init__(self, history_altatest_id, question_altatest_id, answer_id,is_correct, status):
        self.history_altatest_id = history_altatest_id
        self.question_altatest_id = question_altatest_id
        self.answer_id = answer_id
        self.is_correct = is_correct
        self.status = status

    def __rpr__(self):
        return "<Questions %r>" % self.id