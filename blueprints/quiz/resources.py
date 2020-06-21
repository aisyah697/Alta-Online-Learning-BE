import json
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

from .model import Quizs

bp_quiz = Blueprint("quiz", __name__)
api = Api(bp_quiz)


class QuizsResource(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for get quiz by ID
    def get(self, id=None):
        qry_quiz = Quizs.query.filter_by(status=True).filter_by(id=id).first()

        if qry_quiz is not None:
            quiz = marshal(qry_quiz, Quizs.response_fields)
            
            return quiz, 200
        
        return {"status": "Id quiz is not found"}, 404

    #endpoint post quiz
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("exam_id", location="json", required=True)
        parser.add_argument("name", location="json")
        parser.add_argument("description", location="json")
        parser.add_argument("status", location="json", type=bool, default=True)
        args = parser.parse_args()

        quiz_exam = Quizs.query.filter_by(exam_id=args["exam_id"]).first()

        if quiz_exam is not None:
            return {"status": "Exam is already there for this subject"}

        result = Quizs(
            args["exam_id"],
            args["name"],
            args["description"],
            args["status"]
        )

        db.session.add(result)
        db.session.commit()

        return marshal(result, Quizs.response_fields), 200

    #endpoint for soft delete
    def put(self, id):
        #check id in query or not
        qry_quiz = Quizs.query.get(id)
        
        if qry_quiz is None:
            return {'status': 'Quiz is NOT_FOUND'}, 404
        
        #input update status for soft delete
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete      
        qry_quiz.status = args['status']

        db.session.commit()

        return marshal(qry_quiz, Quizs.response_fields), 200

    #endpoint for update quiz
    def patch(self, id):
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

    #Endpoint delete quiz by Id
    def delete(self, id):
        quiz_exam = Quizs.query.get(id)

        if quiz_exam is not None:
            db.session.delete(quiz_exam)
            db.session.commit()

            return {"status": "DELETED SUCCESS"}, 200

        return {"status": "NOT_FOUND"}, 404


class QuizsAll(Resource):
    #endpoint to get all and sort by exam_id
    def get(self):
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


class QuizsAllStatus(Resource):
    #endpoint to get all status of livecode
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