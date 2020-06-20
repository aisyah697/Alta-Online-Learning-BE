from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer

from blueprints.module.model import Modules

class RequirementsModule(db.Model):
    __tablename__ = "requirements_module"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    module_id = db.Column(db.Integer, db.ForeignKey(Modules.id, ondelete="CASCADE"), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "module_id": fields.Integer,
        "description": fields.String,
        "status": fields.Boolean,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime
    }

    def __init__ (self, module_id, description, status):
        self.module_id = module_id
        self.description = description
        self.status = status

    def __rpr__(self):
        return "<Users %r>" % self.id