import json
import os
import werkzeug
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app
from sqlalchemy import desc
# import hashlib, uuid
# from flask_jwt_extended import (
#     JWTManager,
#     create_access_token,
#     get_jwt_identity,
#     jwt_required,
#     get_jwt_claims,
# )

from .model import QuestionsQuiz
from ..quiz.model import Quizs
from ..choice_quiz.model import ChoicesQuiz

bp_question_quiz = Blueprint("question_quiz", __name__)
api = Api(bp_question_quiz)


class QuestionsQuizResource(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for get questions by ID
    def get(self, id=None):
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

    #endpoint post question quiz
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("quiz_id", location="json", required=True)
        parser.add_argument("question", location="json", required=True)
        parser.add_argument("status", location="json", type=bool, default=True)
        args = parser.parse_args()

        #check quiz_id
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

    #endpoint for soft delete
    def put(self, id):
        #check id in query or not
        qry_question_quiz = QuestionsQuiz.query.get(id)
        
        if qry_question_quiz is None:
            return {'status': 'Question quiz is NOT_FOUND'}, 404
        
        #input update status 
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete      
        qry_question_quiz.status = args['status']

        db.session.commit()

        return marshal(qry_question_quiz, QuestionsQuiz.response_fields), 200

    #endpoint for update question
    def patch(self, id):
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

    #endpoint to delete question by id
    def delete(self, id):
        question_quiz = QuestionsQuiz.query.get(id)

        if question_quiz is not None:
            db.session.delete(question_quiz)
            db.session.commit()

            return {"status": "DELETED SUCCESS"}, 200

        return {"status": "NOT_FOUND"}, 404


class QuestionsQuizAll(Resource):
    #endpoint to get all and sort by question and created_at
    def get(self):
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


class QuestionsQuizAllStatus(Resource):
    #endpoint to get all status of question 
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