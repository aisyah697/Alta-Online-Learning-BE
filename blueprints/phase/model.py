from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer

class Phases(db.Model):
    __tablename__ = "phases"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    module = db.relationship("Modules", cascade="all, delete-orphan", passive_deletes=True)
    # module_history = db.relationship("ModuleHistories", cascade="all, delete-orphan", passive_deletes=True)

    response_fields = {
        "id": fields.Integer,
        "name": fields.String,
        "description": fields.String,
        "status": fields.Boolean,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime
    }

    def __init__ (self, name, description, status):
        self.name = name
        self.description = description
        self.status = status

    def __rpr__(self):
        return "<Users %r>" % self.id