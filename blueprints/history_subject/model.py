from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer

from blueprints.subject.model import Subjects
from blueprints.mentee.model import Mentees

class HistoriesSubject(db.Model):
    __tablename__ = "histories_subject"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_id = db.Column(db.Integer, db.ForeignKey(Subjects.id, ondelete="CASCADE"), nullable=False)
    mentee_id = db.Column(db.Integer, db.ForeignKey(Mentees.id, ondelete="CASCADE"), nullable=False)
    score = db.Column(db.Integer)
    is_complete = db.Column(db.Boolean)
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "subject_id": fields.Integer,
        "mentee_id": fields.Integer,
        "score": fields.Integer,
        "is_complete": fields.Boolean,
        "status": fields.Boolean,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime
    }

    def __init__ (self, subject_id, mentee_id, score, is_complete, status):
        self.subject_id = subject_id
        self.mentee_id = mentee_id
        self.score = score
        self.is_complete = is_complete
        self.status = status

    def __rpr__(self):
        return "<Users %r>" % self.id