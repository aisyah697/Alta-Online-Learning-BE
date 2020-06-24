from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer

from blueprints.admin.model import Admins
from blueprints.phase.model import Phases

class Modules(db.Model):
    __tablename__ = "modules"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey(Admins.id, ondelete="CASCADE"), nullable=False)
    phase_id = db.Column(db.Integer, db.ForeignKey(Phases.id, ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(250), nullable=False, unique=True)
    description = db.Column(db.Text)
    image = db.Column(db.String(255))
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    review_module = db.relationship("ReviewsModule", cascade="all, delete-orphan", passive_deletes=True)
    requirement_module = db.relationship("RequirementsModule", cascade="all, delete-orphan", passive_deletes=True)
    subject = db.relationship("Subjects", cascade="all, delete-orphan", passive_deletes=True)
    history_module = db.relationship("HistoriesModule", cascade="all, delete-orphan", passive_deletes=True)

    response_fields = {
        "id": fields.Integer,
        "admin_id": fields.Integer,
        "phase_id": fields.Integer,
        "name": fields.String,
        "description": fields.String,
        "image": fields.String,
        "status": fields.Boolean,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime
    }

    def __init__ (self, admin_id, phase_id, name, description, image, status):
        self.admin_id = admin_id
        self.phase_id = phase_id
        self.name = name
        self.description = description
        self.image = image
        self.status = status

    def __rpr__(self):
        return "<Users %r>" % self.id