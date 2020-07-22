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

from .model import ChoicesQuiz
from ..question_quiz.model import QuestionsQuiz
from ..quiz.model import Quizs

bp_choice_quiz = Blueprint("choice_quiz", __name__)
api = Api(bp_choice_quiz)


class ChoicesQuizResource(Resource):
    # Endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    # Endpoint for get choices by ID
    @admin_required
    def get(self, id=None):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            qry_choice_quiz = ChoicesQuiz.query.filter_by(status=True).filter_by(id=id).first()

            if qry_choice_quiz is not None:
                choice_quiz = marshal(qry_choice_quiz, ChoicesQuiz.response_fields)
                
                return choice_quiz, 200
            
            return {"status": "Id Choice Quiz is not found"}, 404

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    # Endpoint post choice quiz
    @admin_required
    def post(self):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            parser = reqparse.RequestParser()
            parser.add_argument("question_id", location="json", required=True)
            parser.add_argument("choice", location="json", required=True)
            parser.add_argument("is_correct", location="json", type=bool, default=False)
            parser.add_argument("status", location="json", type=bool, default=True)
            args = parser.parse_args()

            qry_question_quiz = QuestionsQuiz.query.get(args["question_id"])
            if qry_question_quiz is None:
                return {"status": "Question for this choice is Not Found"}, 404

            result = ChoicesQuiz(
                args["question_id"],
                args["choice"],
                args["is_correct"],
                args["status"]
            )

            db.session.add(result)
            db.session.commit()

            return marshal(result, ChoicesQuiz.response_fields), 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    # Endpoint for soft delete
    def put(self, id):
        # Check id in query or not
        qry_choice_quiz = ChoicesQuiz.query.get(id)
        
        if qry_choice_quiz is None:
            return {'status': 'Choice Quiz is NOT_FOUND'}, 404
        
        # Input update status for soft delete
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        # Change status for soft delete      
        qry_choice_quiz.status = args['status']

        db.session.commit()

        return marshal(qry_choice_quiz, ChoicesQuiz.response_fields), 200

    # Endpoint for update choice
    @admin_required
    def patch(self, id):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            qry_choice_quiz = ChoicesQuiz.query.filter_by(status=True).filter_by(id=id).first()
            if qry_choice_quiz is None:
                return {'status': 'Choice Quiz is NOT_FOUND'}, 404

            parser = reqparse.RequestParser()
            parser.add_argument("choice", location="json")
            parser.add_argument("is_correct", location="json", type=bool)
            args = parser.parse_args()

            if args['choice'] is not None:
                qry_choice_quiz.choice = args['choice']

            if args['is_correct'] is not None:
                qry_choice_quiz.is_correct = args['is_correct']

            db.session.commit()

            return marshal(qry_choice_quiz, ChoicesQuiz.response_fields), 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    # Endpoint delete Choice Quiz by Id
    @admin_required
    def delete(self, id):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            choice_quiz = ChoicesQuiz.query.get(id)

            if choice_quiz is not None:
                db.session.delete(choice_quiz)
                db.session.commit()

                return {"status": "DELETED SUCCESS"}, 200

            return {"status": "NOT_FOUND"}, 404

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class ChoicesQuizAll(Resource):
    # Endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    # Endpoint to get all and sort by choice and created_at
    @admin_required
    def get(self):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=25)
            parser.add_argument('orderby', location='args', help='invalid status', choices=("choice", "created_at"))
            parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']

            qry_choice_quiz = ChoicesQuiz.query

            if args["orderby"] is not None:
                if args['orderby'] == "choice":
                    if args["sort"] == "desc":
                        qry_choice_quiz = qry_choice_quiz.order_by(desc(ChoicesQuiz.choice))
                    else:
                        qry_choice_quiz = qry_choice_quiz.order_by(ChoicesQuiz.choice)
                elif args["orderby"] == "created_at":
                    if args["sort"] == "desc":
                        qry_choice_quiz = qry_choice_quiz.order_by(desc(ChoicesQuiz.created_at))
                    else:
                        qry_choice_quiz = qry_choice_quiz.order_by(ChoicesQuiz.created_at)

            rows = []
            for row in qry_choice_quiz.limit(args['rp']).offset(offset).all():
                if row.status == True:
                    row = marshal(row, ChoicesQuiz.response_fields)
                    rows.append(row)

            return rows, 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class ChoicesQuizAllStatus(Resource):
    # Endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200
    
    # Endpoint to get all status of choice 
    def get(self):
        qry_choice_quiz = ChoicesQuiz.query

        rows = []
        for row in qry_choice_quiz:
            row = marshal(row, ChoicesQuiz.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200


api.add_resource(ChoicesQuizAll, "")
api.add_resource(ChoicesQuizResource, "", "/<id>")
api.add_resource(ChoicesQuizAllStatus, "", "/all")