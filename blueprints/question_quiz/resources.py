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

from .model import QuestionsQuiz
from ..quiz.model import Quizs
from ..choice_quiz.model import ChoicesQuiz

bp_question_quiz = Blueprint("question_quiz", __name__)
api = Api(bp_question_quiz)


class QuestionsQuizResource(Resource):
    # Endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    # Endpoint for get questions by ID
    @admin_required
    def get(self, id=None):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            qry_question_quiz = QuestionsQuiz.query.filter_by(status=True).filter_by(id=id).first()

            if qry_question_quiz is not None:
                qry_choice_quiz = ChoicesQuiz.query.filter_by(question_id=qry_question_quiz.id).all()
                
                rows = []
                for row in qry_choice_quiz:
                    rows.append(marshal(row, ChoicesQuiz.response_fields))
                
                result_question_quiz = marshal(qry_question_quiz, QuestionsQuiz.response_fields)
                
                if rows != []:
                    result_question_quiz["choice_id"] = rows
                
                return result_question_quiz, 200
            
            return {"status": "Id Question Quiz is not found"}, 404

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    # Endpoint post question quiz
    @admin_required
    def post(self):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            parser = reqparse.RequestParser()
            parser.add_argument("quiz_id", location="json", required=True)
            parser.add_argument("question", location="json", required=True)
            parser.add_argument("status", location="json", type=bool, default=True)
            args = parser.parse_args()

            # Check quiz_id
            quiz_id = Quizs.query.get(args["quiz_id"])

            if quiz_id is None:
                return {"status": "Quiz isn't in database"}, 404

            result = QuestionsQuiz(
                args["quiz_id"],
                args["question"],
                args["status"]
            )

            db.session.add(result)
            db.session.commit()

            return marshal(result, QuestionsQuiz.response_fields), 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    # Endpoint for soft delete
    def put(self, id):
        # Check id in query or not
        qry_question_quiz = QuestionsQuiz.query.get(id)
        
        if qry_question_quiz is None:
            return {'status': 'Question quiz is NOT_FOUND'}, 404
        
        # Input update status 
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        # Change status for soft delete      
        qry_question_quiz.status = args['status']

        db.session.commit()

        return marshal(qry_question_quiz, QuestionsQuiz.response_fields), 200

    # Endpoint for update question
    @admin_required
    def patch(self, id):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            qry_question_quiz = QuestionsQuiz.query.filter_by(status=True).filter_by(id=id).first()
            if qry_question_quiz is None:
                return {'status': 'Question Quiz is NOT_FOUND'}, 404

            parser = reqparse.RequestParser()
            parser.add_argument("question", location="json")
            args = parser.parse_args()

            if args['question'] is not None:
                qry_question_quiz.question = args['question']

            db.session.commit()

            return marshal(qry_question_quiz, QuestionsQuiz.response_fields), 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    # Endpoint to delete question by id
    @admin_required
    def delete(self, id):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            question_quiz = QuestionsQuiz.query.get(id)

            if question_quiz is not None:
                db.session.delete(question_quiz)
                db.session.commit()

                return {"status": "DELETED SUCCESS"}, 200

            return {"status": "NOT_FOUND"}, 404

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class QuestionsQuizAll(Resource):
    # Endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    # Endpoint to get all and sort by question and created_at
    @admin_required
    def get(self):
        # Check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=25)
            parser.add_argument('orderby', location='args', help='invalid status', choices=("question", "created_at"))
            parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']

            qry_question_quiz = QuestionsQuiz.query

            if args["orderby"] is not None:
                if args['orderby'] == "question":
                    if args["sort"] == "desc":
                        qry_question_quiz = qry_question_quiz.order_by(desc(QuestionsQuiz.question))
                    else:
                        qry_question_quiz = qry_question_quiz.order_by(QuestionsQuiz.question)
                elif args["orderby"] == "created_at":
                    if args["sort"] == "desc":
                        qry_question_quiz = qry_question_quiz.order_by(desc(QuestionsQuiz.created_at))
                    else:
                        qry_question_quiz = qry_question_quiz.order_by(QuestionsQuiz.created_at)

            rows = []
            for row in qry_question_quiz.limit(args['rp']).offset(offset).all():
                if row.status == True:
                    row = marshal(row, QuestionsQuiz.response_fields)
                    rows.append(row)

            return rows, 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class QuestionsQuizAllStatus(Resource):
    # Endpoint to get all status of question 
    def get(self):
        qry_question_quiz = QuestionsQuiz.query

        rows = []
        for row in qry_question_quiz:
            row = marshal(row, QuestionsQuiz.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200

api.add_resource(QuestionsQuizAll, "")
api.add_resource(QuestionsQuizResource, "", "/<id>")
api.add_resource(QuestionsQuizAllStatus, "", "/all")