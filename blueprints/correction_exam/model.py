from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer

from blueprints.history_exam.model import HistoriesExam

class CorrectionsExam(db.Model):
    __tablename__ = "corrections_exam"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    history_exam_id = db.Column(db.Integer, db.ForeignKey(HistoriesExam.id, ondelete="CASCADE"), nullable=False)
    question_quiz_id = db.Column(db.Integer)
    answer_quiz_id = db.Column(db.Integer)
    is_correct = db.Column(db.Boolean)
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "history_exam_id": fields.Integer,
        "question_quiz_id": fields.Integer,
        "answer_quiz_id": fields.Integer,
        "is_correct": fields.Boolean,
        "status": fields.Boolean,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime,
    }

    def __init__(self, history_exam_id, question_quiz_id, answer_quiz_id, is_correct, status):
        self.history_exam_id = history_exam_id
        self.question_quiz_id = question_quiz_id
        self.answer_quiz_id = answer_quiz_id
        self.is_correct = is_correct
        self.status = status

    def __rpr__(self):
        return "<Questions %r>" % self.id