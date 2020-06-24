from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer

class Altatests(db.Model):
    __tablename__ = "altatests"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_sum = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    altatest_history = db.relationship("HistoriesAltatest", cascade="all, delete-orphan", passive_deletes=True)

    response_fields = {
        "id": fields.Integer,
        "question_sum": fields.Integer,
        "status": fields.Boolean,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime
    }

    def __init__ (self, question_sum, status):
        self.question_sum = question_sum
        self.status = status

    def __rpr__(self):
        return "<Users %r>" % self.id