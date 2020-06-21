from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer

from blueprints.subject.model import Subjects

class Exams(db.Model):
    __tablename__ = "exams"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_id = db.Column(db.Integer, db.ForeignKey(Subjects.id, ondelete="CASCADE"), nullable=False)
    type_exam = db.Column(db.String(250), nullable=False)
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    # quiz = db.relationship("Quizs", cascade="all, delete-orphan", passive_deletes=True)
    # livecode = db.relationship("Livecodes", cascade="all, delete-orphan", passive_deletes=True)

    response_fields = {
        "id": fields.Integer,
        "subject_id": fields.Integer,
        "type_exam": fields.String,
        "status": fields.Boolean,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime
    }

    def __init__ (self, subject_id, type_exam, status):
        self.subject_id = subject_id
        self.type_exam = type_exam
        self.status = status

    def __rpr__(self):
        return "<Users %r>" % self.id