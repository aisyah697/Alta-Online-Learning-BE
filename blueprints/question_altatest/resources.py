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

from .model import QuestionsAltatest
from ..admin.model import Admins
from ..choice_altatest.model import ChoicesAltatest

bp_question_altatest = Blueprint("question_altatest", __name__)
api = Api(bp_question_altatest)


class QuestionsAltatestResource(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for get questions by ID
    def get(self, id=None):
        qry_question_altatest = QuestionsAltatest.query.filter_by(status=True).filter_by(id=id).first()

        if qry_question_altatest is not None:
            qry_choice_altatest = ChoicesAltatest.query.filter_by(question_id=qry_question_altatest.id).all()
            
            rows = []
            for row in qry_choice_altatest:
                rows.append(marshal(row, ChoicesAltatest.response_fields))
            
            result_question_altatest = marshal(qry_question_altatest, QuestionsAltatest.response_fields)
            
            if rows != []:
                result_question_altatest["choice_id"] = rows
            
            return result_question_altatest, 200
        
        return {"status": "Id Question Altatest is not found"}, 404

    #endpoint post question altatest
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("admin_id", location="json", required=True)
        parser.add_argument("question", location="json", required=True)
        parser.add_argument("status", location="json", type=bool, default=True)
        args = parser.parse_args()

        qry_admin = Admins.query.get(args["admin_id"])
        admin = marshal(qry_admin, Admins.response_fields)

        result = QuestionsAltatest(
            args["admin_id"],
            args["question"],
            args["status"]
        )

        db.session.add(result)
        db.session.commit()

        return marshal(result, QuestionsAltatest.response_fields), 200

    #endpoint for soft delete
    def put(self, id):
        #check id in query or not
        qry_question_altatest = QuestionsAltatest.query.get(id)
        
        if qry_question_altatest is None:
            return {'status': 'Question Altatest is NOT_FOUND'}, 404
        
        #input update status 
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete      
        qry_question_altatest.status = args['status']

        db.session.commit()

        return marshal(qry_question_altatest, QuestionsAltatest.response_fields), 200

    #endpoint for update question
    def patch(self, id):
        qry_question_altatest = QuestionsAltatest.query.filter_by(status=True).filter_by(id=id).first()
        if qry_question_altatest is None:
            return {'status': 'Question Altatest is NOT_FOUND'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument("question", location="json")
        args = parser.parse_args()

        if args['question'] is not None:
            qry_question_altatest.question = args['question']

        db.session.commit()

        return marshal(qry_question_altatest, QuestionsAltatest.response_fields), 200

    #endpoint to delete question by id
    def delete(self, id):
        question_altatest = QuestionsAltatest.query.get(id)

        if question_altatest is not None:
            db.session.delete(question_altatest)
            db.session.commit()

            return {"status": "DELETED SUCCESS"}, 200

        return {"status": "NOT_FOUND"}, 404


class QuestionsAltatestAll(Resource):
    #endpoint to get all and sort by question and created_at
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=("question", "created_at"))
        parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry_question_altatest = QuestionsAltatest.query

        if args["orderby"] is not None:
            if args['orderby'] == "question":
                if args["sort"] == "desc":
                    qry_question_altatest = qry_question_altatest.order_by(desc(QuestionsAltatest.question))
                else:
                    qry_question_altatest = qry_question_altatest.order_by(QuestionsAltatest.question)
            elif args["orderby"] == "created_at":
                if args["sort"] == "desc":
                    qry_question_altatest = qry_question_altatest.order_by(desc(QuestionsAltatest.created_at))
                else:
                    qry_question_altatest = qry_question_altatest.order_by(QuestionsAltatest.created_at)

        rows = []
        for row in qry_question_altatest.limit(args['rp']).offset(offset).all():
            if row.status == True:
                row = marshal(row, QuestionsAltatest.response_fields)
                rows.append(row)

        return rows, 200


class QuestionsAltatestAllStatus(Resource):
    #endpoint to get all status of question 
    def get(self):
        qry_question_altatest = QuestionsAltatest.query

        rows = []
        for row in qry_question_altatest:
            row = marshal(row, QuestionsAltatest.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200

api.add_resource(QuestionsAltatestAll, "")
api.add_resource(QuestionsAltatestResource, "", "/<id>")
api.add_resource(QuestionsAltatestAllStatus, "", "/all")