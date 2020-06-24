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

from .model import HistoriesExam
from ..mentee.model import Mentees
from ..exam.model import Exams

bp_history_exam = Blueprint("history_exam", __name__)
api = Api(bp_history_exam)


class HistoriesExamResource(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for search history exam by id
    def get(self, id=None):
        qry_history_exam = HistoriesExam.query.filter_by(status=True).filter_by(id=id).first()

        if qry_history_exam is not None:
            return marshal(qry_history_exam, HistoriesExam.response_fields), 200
        
        return {"status": "Id history exam not found"}, 404

    #endpoint for post history exam
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("exam_id", location="json", required=True)
        parser.add_argument("mentee_id", location="json", required=True)
        parser.add_argument("score", location="json")
        parser.add_argument("status", location="json", type=bool, default=True)
        args = parser.parse_args()


        #Check subject and mentee is existance in database
        qry_history_exam = HistoriesExam.query.filter_by(exam_id=args["exam_id"]).filter_by(mentee_id=args["mentee_id"]).filter_by(status=True).all()
        if len(qry_history_exam) >= 3:
            return {"status": "Exam and Mentee is there 3 times"}, 404

        #Check Id Exam is in database or not
        qry_exam = Exams.query.get(args["exam_id"])
        if qry_exam is None:
            return {"status": "ID Exam is Not Found"}, 404
        
        #Check Id Mentee is in database or not
        qry_mentee = Mentees.query.get(args["mentee_id"])
        if qry_mentee is None:
            return {"status": "ID Mentee is Not Found"}, 404

        result = HistoriesExam(
            args["exam_id"],
            args["mentee_id"],
            args["score"],
            args["status"]
        )

        db.session.add(result)
        db.session.commit()

        return marshal(result, HistoriesExam.response_fields), 200

    #endpoint for soft delete
    def put(self, id):
        #check id in querry or not
        qry_history_exam = HistoriesExam.query.get(id)
        if qry_history_exam is None:
            return {'status': 'History Exam is NOT_FOUND'}, 404

        #input update status
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete
        if args['status'] is not None:
            qry_history_exam.status = args['status']

        db.session.commit()

        return marshal(qry_history_exam, HistoriesExam.response_fields), 200

    #endpoint for update field
    def patch(self, id):
        qry_history_exam = HistoriesExam.query.filter_by(status=True).filter_by(id=id).first()
        if qry_history_exam is None:
            return {'status': 'History Exam is NOT_FOUND'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument("exam_id", location="json")
        parser.add_argument("mentee_id", location="json")
        parser.add_argument("score", location="json")
        args = parser.parse_args()

        if args['exam_id'] is not None:
            qry_history_exam.exam_id = args["exam_id"]

        if args['mentee_id'] is not None:
            qry_history_exam.mentee_id = args['mentee_id']
        
        if args['score'] is not None:
            qry_history_exam.score = args['score']

        db.session.commit()

        return marshal(qry_history_exam, HistoriesExam.response_fields), 200

    #endpoint for delete history subject by id
    def delete(self, id):
        qry_history_exam = HistoriesExam.query.get(id)
        
        if qry_history_exam is not None:
            db.session.delete(qry_history_exam)
            db.session.commit()

            return {"status": "DELETED SUCCESS"}, 200
        
        return {"status": "ID NOT FOUND"}, 200


class HistoriesExamAll(Resource):
    #endpoint to get all and sort by score and created at
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=("score", "created_at"))
        parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry_history_exam = HistoriesExam.query

        if args["orderby"] is not None:
            if args['orderby'] == "score":
                if args["sort"] == "desc":
                    qry_history_exam = qry_history_exam.order_by(desc(HistoriesExam.score))
                else:
                    qry_history_exam = qry_history_exam.order_by(HistoriesExam.score)
            if args['orderby'] == "created_at":
                if args["sort"] == "desc":
                    qry_history_exam = qry_history_exam.order_by(desc(HistoriesExam.created_at))
                else:
                    qry_history_exam = qry_history_exam.order_by(HistoriesExam.created_at)

        rows = []
        for row in qry_history_exam.limit(args['rp']).offset(offset).all():
            if row.status == True:
                row = marshal(row, HistoriesExam.response_fields)
                rows.append(row)

        return rows, 200


class HistoriesExamAllStatus(Resource):
    #endpoint to get all status of history exam
    def get(self):
        qry_history_exam = HistoriesExam.query

        rows = []
        for row in qry_history_exam:
            row = marshal(row, HistoriesExam.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200

api.add_resource(HistoriesExamAll, "")
api.add_resource(HistoriesExamResource, "", "/<id>")
api.add_resource(HistoriesExamAllStatus, "", "/all")