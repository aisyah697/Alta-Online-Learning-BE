import json
import os
import werkzeug
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app
from sqlalchemy import desc
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    verify_jwt_in_request,
    jwt_required,
    get_jwt_claims,
)
from blueprints import admin_required

from .model import Exams
from ..subject.model import Subjects

bp_exam = Blueprint("exam", __name__)
api = Api(bp_exam)


class ExamsResource(Resource):
    # For solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    # Endpoint for search exam by id
    @admin_required
    def get(self, id=None):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            qry_exam = Exams.query.filter_by(status=True).filter_by(id=id).first()

            if qry_exam is not None:
                return marshal(qry_exam, Exams.response_fields), 200
            
            return {"status": "Id Exam not found"}, 404

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    # Endpoint for post exam
    @admin_required
    def post(self):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            parser = reqparse.RequestParser()
            parser.add_argument("subject_id", location="json", required=True)
            parser.add_argument("type_exam", location="json", help='type of exam not available', choices=("quiz", "livecode"))
            parser.add_argument("status", location="json", type=bool, default=True)
            args = parser.parse_args()

            # Check subject_id
            subject_id = Subjects.query.get(args["subject_id"])

            if subject_id is None:
                return {"status": "Subject isn't in database"}, 404

            # Check there no same subject_id
            subject_id_exam = Exams.query.filter_by(subject_id=args["subject_id"]).first()
            
            if subject_id_exam is not None:
                return {"status": "Exam for this subject is already there"}, 404

            result = Exams(
                args["subject_id"],
                args["type_exam"],
                args["status"]
            )

            db.session.add(result)
            db.session.commit()

            return marshal(result, Exams.response_fields), 200
        
        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    # Endpoint for soft delete
    def put(self, id):
        # Check id in query or not
        qry_exam = Exams.query.get(id)
        
        if qry_exam is None:
            return {'status': 'Exam is NOT_FOUND'}, 404
        
        # Input update status for soft delete
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        # Change status for soft delete
        if args["status"] is not None:      
            qry_exam.status = args['status']

        db.session.commit()

        return marshal(qry_exam, Exams.response_fields), 200

    # Endpoint for update field
    @admin_required
    def patch(self, id):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":        
            # Check id in querry or not
            qry_exam = Exams.query.filter_by(status=True).filter_by(id=id).first()
            if qry_exam is None:
                return {'status': 'Exam is NOT_FOUND'}, 404

            parser = reqparse.RequestParser()
            parser.add_argument("subject_id", location="json")
            parser.add_argument("type_exam", location="json", help='type of exam not available', choices=("quiz", "livecode"))
            args = parser.parse_args()

            if args['subject_id'] is not None:
                qry_exam.subject_id = args["subject_id"]
            
            if args['type_exam'] is not None:
                qry_exam.type_exam = args["type_exam"]
            
            db.session.commit()

            return marshal(qry_exam, Exams.response_fields), 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    # Endpoint delete file subject by Id
    @admin_required
    def delete(self, id):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":        
            qry_exam = Exams.query.get(id)

            if qry_exam is not None:
                db.session.delete(qry_exam)
                db.session.commit()

                return {"status": "DELETED SUCCESS"}, 200

            return {"status": "NOT_FOUND"}, 404

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class ExamsAll(Resource):
    # Endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    # Endpoint to get all and sort by subject_id and type_exam
    @admin_required
    def get(self):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=25)
            parser.add_argument('orderby', location='args', help='invalid status', choices=("subject_id", "type_exam"))
            parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']

            qry_exam = Exams.query

            if args["orderby"] is not None:
                if args['orderby'] == "subject_id":
                    if args["sort"] == "desc":
                        qry_exam = qry_exam.order_by(desc(Exams.subject_id))
                    else:
                        qry_exam = qry_exam.order_by(Exams.subject_id)
                if args['orderby'] == "type_exam":
                    if args["sort"] == "desc":
                        qry_exam = qry_exam.order_by(desc(Exams.type_exam))
                    else:
                        qry_exam = qry_exam.order_by(Exams.type_exam)

            rows = []
            for row in qry_exam.limit(args['rp']).offset(offset).all():
                if row.status == True:
                    row = marshal(row, Exams.response_fields)
                    rows.append(row)

            return rows, 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class ExamsAllStatus(Resource):
    # Endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    # Endpoint to get all status of exa,
    def get(self):
        qry_exam = Exams.query

        rows = []
        for row in qry_exam:
            row = marshal(row, Exams.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200

api.add_resource(ExamsAll, "")
api.add_resource(ExamsResource, "", "/<id>")
api.add_resource(ExamsAllStatus, "", "/all")