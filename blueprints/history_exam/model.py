from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer

from blueprints.exam.model import Exams
from blueprints.mentee.model import Mentees

class HistoriesExam(db.Model):
    __tablename__ = "histories_exam"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exam_id = db.Column(db.Integer, db.ForeignKey(Exams.id, ondelete="CASCADE"), nullable=False)
    mentee_id = db.Column(db.Integer, db.ForeignKey(Mentees.id, ondelete="CASCADE"), nullable=False)
    score = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "exam_id": fields.Integer,
        "mentee_id": fields.Integer,
        "score": fields.Integer,
        "status": fields.Boolean,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime
    }

    def __init__ (self, exam_id, mentee_id, score, status):
        self.exam_id = exam_id
        self.mentee_id = mentee_id
        self.score = score
        self.status = status

    def __rpr__(self):
        return "<Users %r>" % self.id