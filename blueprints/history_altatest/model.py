from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer

from blueprints.altatest.model import Altatests
from blueprints.mentee.model import Mentees


class HistoriesAltatest(db.Model):
    __tablename__ = "histories_altatest"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    altatest_id = db.Column(db.Integer, db.ForeignKey(Altatests.id, ondelete="CASCADE"), nullable=True)
    mentee_id = db.Column(db.Integer, db.ForeignKey(Mentees.id, ondelete="CASCADE"), nullable=True)
    score = db.Column(db.Integer)
    time_start = db.Column(db.DateTime)
    is_complete = db.Column(db.String(10))
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    correction_altatest = db.relationship("CorrectionsAltatest", cascade="all, delete-orphan", passive_deletes=True)

    response_fields = {
        "id": fields.Integer,
        "altatest_id": fields.Integer,
        "mentee_id": fields.Integer,
        "score": fields.Integer,
        "time_start": fields.DateTime,
        "is_complete": fields.String,
        "status": fields.Boolean,
        "created_at": fields.DateTime,
        "updated_at": fields.DateTime
    }

    def __init__ (self, altatest_id, mentee_id, score, time_start, is_complete, status):
        self.altatest_id = altatest_id
        self.mentee_id = mentee_id
        self.score = score
        self.time_start = time_start
        self.is_complete = is_complete
        self.status = status

    def __rpr__(self):
        return "<Users %r>" % self.id
