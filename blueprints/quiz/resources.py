import json
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

from .model import Quizs
from ..exam.model import Exams

bp_quiz = Blueprint("quiz", __name__)
api = Api(bp_quiz)


class QuizsResource(Resource):
    # Endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    # Endpoint for get quiz by ID
    @admin_required
    def get(self, id=None):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            qry_quiz = Quizs.query.filter_by(status=True).filter_by(id=id).first()

            if qry_quiz is not None:
                quiz = marshal(qry_quiz, Quizs.response_fields)
                
                return quiz, 200
            
            return {"status": "Id quiz is not found"}, 404

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    # Endpoint post quiz
    @admin_required
    def post(self):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            parser = reqparse.RequestParser()
            parser.add_argument("exam_id", location="json", required=True)
            parser.add_argument("name", location="json")
            parser.add_argument("description", location="json")
            parser.add_argument("status", location="json", type=bool, default=True)
            args = parser.parse_args()

            # Check exam_id
            exam_id = Exams.query.get(args["exam_id"])

            if exam_id is None:
                return {"status": "Exam isn't in database"}, 404

            # Check there no same exam_id
            exam_id_quiz = Quizs.query.filter_by(exam_id=args["exam_id"]).first()
            
            if exam_id_quiz is not None:
                return {"status": "Quiz for this exam is already there"}, 404

            result = Quizs(
                args["exam_id"],
                args["name"],
                args["description"],
                args["status"]
            )

            db.session.add(result)
            db.session.commit()

            return marshal(result, Quizs.response_fields), 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    # Endpoint for soft delete
    def put(self, id):
        # Check id in query or not
        qry_quiz = Quizs.query.get(id)
        
        if qry_quiz is None:
            return {'status': 'Quiz is NOT_FOUND'}, 404
        
        # Input update status for soft delete
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        # Change status for soft delete      
        qry_quiz.status = args['status']

        db.session.commit()

        return marshal(qry_quiz, Quizs.response_fields), 200

    # Endpoint for update quiz
    @admin_required
    def patch(self, id):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            qry_quiz = Quizs.query.filter_by(status=True).filter_by(id=id).first()
            if qry_quiz is None:
                return {'status': 'Quiz is NOT_FOUND'}, 404

            parser = reqparse.RequestParser()
            parser.add_argument("exam_id", location="json")
            parser.add_argument("name", location="json")
            parser.add_argument("description", location="json")
            args = parser.parse_args()

            if args['exam_id'] is not None:
                qry_quiz.exam_id = args['exam_id']

            if args['name'] is not None:
                qry_quiz.name = args['name']

            if args['description'] is not None:
                qry_quiz.description = args['description']

            db.session.commit()

            return marshal(qry_quiz, Quizs.response_fields), 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    # Endpoint delete quiz by Id
    @admin_required
    def delete(self, id):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            quiz_exam = Quizs.query.get(id)

            if quiz_exam is not None:
                db.session.delete(quiz_exam)
                db.session.commit()

                return {"status": "DELETED SUCCESS"}, 200

            return {"status": "NOT_FOUND"}, 404

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class QuizsAll(Resource):
    # Endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200
    
    # Endpoint to get all and sort by exam_id
    @admin_required
    def get(self):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=25)
            parser.add_argument('orderby', location='args', help='invalid status', choices=("exam_id"))
            parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']

            qry_quiz = Quizs.query

            if args["orderby"] is not None:
                if args['orderby'] == "exam_id":
                    if args["sort"] == "desc":
                        qry_quiz = qry_quiz.order_by(desc(Quizs.exam_id))
                    else:
                        qry_quiz = qry_quiz.order_by(Quizs.exam_id)
                
            rows = []
            for row in qry_quiz.limit(args['rp']).offset(offset).all():
                if row.status == True:
                    row = marshal(row, Quizs.response_fields)
                    rows.append(row)

            return rows, 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class QuizsAllStatus(Resource):
    # Endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    # Endpoint to get all status of livecode
    def get(self):
        qry_quiz = Quizs.query

        rows = []
        for row in qry_quiz:
            row = marshal(row, Quizs.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200


api.add_resource(QuizsAll, "")
api.add_resource(QuizsResource, "", "/<id>")
api.add_resource(QuizsAllStatus, "", "/all")