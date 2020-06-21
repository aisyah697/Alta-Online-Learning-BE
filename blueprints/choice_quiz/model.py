from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer

from blueprints.question_quiz.model import QuestionsQuiz


class ChoicesQuiz(db.Model):
    __tablename__ = "choices_quiz"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey(QuestionsQuiz.id, ondelete="CASCADE"), nullable=False)
    choice = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean)
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "question_id": fields.Integer,
        "choice": fields.String,
        "is_correct": fields.Boolean,
        "status": fields.Boolean,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime,
    }

    def __init__(self, question_id, choice, is_correct, status):
        self.question_id =  question_id
        self.choice = choice
        self.is_correct = is_correct
        self.status = status

    def __rpr__(self):
        return "<Questions %r>" % self.id