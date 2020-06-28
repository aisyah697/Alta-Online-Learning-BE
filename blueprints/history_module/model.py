from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer

from blueprints.module.model import Modules
from blueprints.mentee.model import Mentees

class HistoriesModule(db.Model):
    __tablename__ = "histories_module"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    module_id = db.Column(db.Integer, db.ForeignKey(Modules.id, ondelete="CASCADE"), nullable=False)
    mentee_id = db.Column(db.Integer, db.ForeignKey(Mentees.id, ondelete="CASCADE"), nullable=False)
    score = db.Column(db.Integer)
    is_complete = db.Column(db.Boolean)
    lock_key = db.Column(db.Boolean)
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "module_id": fields.Integer,
        "mentee_id": fields.Integer,
        "score": fields.Integer,
        "is_complete": fields.Boolean,
        "lock_key": fields.Boolean,
        "status": fields.Boolean,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime
    }

    def __init__ (self, module_id, mentee_id, score, is_complete, lock_key, status):
        self.module_id = module_id
        self.mentee_id = mentee_id
        self.score = score
        self.is_complete = is_complete
        self.lock_key = lock_key
        self.status = status

    def __rpr__(self):
        return "<Users %r>" % self.id