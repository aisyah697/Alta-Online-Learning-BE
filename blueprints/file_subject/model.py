from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer

from blueprints.subject.model import Subjects

class FilesSubject(db.Model):
    __tablename__ = "files_subject"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_id = db.Column(db.Integer, db.ForeignKey(Subjects.id, ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(250))
    content_file = db.Column(db.String(250), nullable=False)
    category_file = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "subject_id": fields.Integer,
        "name": fields.String,
        "content_file": fields.String,
        "category_file": fields.String,
        "status": fields.Boolean,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime
    }

    def __init__ (self, subject_id, name, content_file, category_file, status):
        self.subject_id = subject_id
        self.name = name
        self.content_file = content_file
        self.category_file = category_file
        self.status = status

    def __rpr__(self):
        return "<Users %r>" % self.id