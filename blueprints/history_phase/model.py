from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer

from blueprints.phase.model import Phases
from blueprints.mentee.model import Mentees

class HistoriesPhase(db.Model):
    __tablename__ = "histories_phase"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phase_id = db.Column(db.Integer, db.ForeignKey(Phases.id, ondelete="CASCADE"), nullable=False)
    mentee_id = db.Column(db.Integer, db.ForeignKey(Mentees.id, ondelete="CASCADE"), nullable=False)
    score = db.Column(db.Integer)
    certificate = db.Column(db.String(250))
    lock_key = db.Column(db.Boolean)
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "phase_id": fields.Integer,
        "mentee_id": fields.Integer,
        "score": fields.Integer,
        "certificate": fields.String,
        "lock_key": fields.Boolean,
        "status": fields.Boolean,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime
    }

    def __init__ (self, phase_id, mentee_id, score, certificate, lock_key, status):
        self.phase_id = phase_id
        self.mentee_id = mentee_id
        self.score = score
        self.certificate = certificate
        self.lock_key = lock_key
        self.status = status

    def __rpr__(self):
        return "<Users %r>" % self.id