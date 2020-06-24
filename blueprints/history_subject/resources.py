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

from .model import HistoriesSubject
from ..mentee.model import Mentees
from ..subject.model import Subjects

bp_history_subject = Blueprint("history_subject", __name__)
api = Api(bp_history_subject)


class HistoriesSubjectResource(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for search history subject by id
    def get(self, id=None):
        qry_history_subject = HistoriesSubject.query.filter_by(status=True).filter_by(id=id).first()

        if qry_history_subject is not None:
            return marshal(qry_history_subject, HistoriesSubject.response_fields), 200
        
        return {"status": "Id history subject not found"}, 404

    #endpoint for post history subject
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("subject_id", location="json", required=True)
        parser.add_argument("mentee_id", location="json", required=True)
        parser.add_argument("score", location="json")
        parser.add_argument("status", location="json", type=bool, default=True)
        args = parser.parse_args()

        #Check subject and mentee is existance in database
        qry_history_subject = HistoriesSubject.query.filter_by(subject_id=args["subject_id"]).filter_by(mentee_id=args["mentee_id"]).filter_by(status=True).all()
        if len(qry_history_subject) > 0:
            return {"status": "Subject and Mentee is already there"}, 404

        #Check Id Mentee is in database or not
        qry_mentee = Mentees.query.get(args["mentee_id"])
        if qry_mentee is None:
            return {"status": "ID Mentee is Not Found"}, 404

        #Check Id Subject is in database or not
        qry_subject = Subjects.query.get(args["subject_id"])
        if qry_subject is None:
            return {"status": "ID Subject is Not Found"}, 404

        if int(args["score"]) >= 80:
            args["is_complete"] = True
        else:
            args["is_complete"] = False

        result = HistoriesSubject(
            args["subject_id"],
            args["mentee_id"],
            args["score"],
            args["is_complete"],
            args["status"]
        )

        db.session.add(result)
        db.session.commit()

        return marshal(result, HistoriesSubject.response_fields), 200

    #endpoint for soft delete
    def put(self, id):
        #check id in querry or not
        qry_history_subject = HistoriesSubject.query.get(id)
        if qry_history_subject is None:
            return {'status': 'History Subject is NOT_FOUND'}, 404

        #input update status 
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete
        if args['status'] is not None:
            qry_history_subject.status = args['status']

        db.session.commit()

        return marshal(qry_history_subject, HistoriesSubject.response_fields), 200

    #endpoint for update field
    def patch(self, id):
        qry_history_subject = HistoriesSubject.query.filter_by(status=True).filter_by(id=id).first()
        if qry_history_subject is None:
            return {'status': 'History Subject is NOT_FOUND'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument("subject_id", location="json")
        parser.add_argument("mentee_id", location="json")
        parser.add_argument("score", location="json")
        args = parser.parse_args()

        if args['subject_id'] is not None:
            qry_history_subject.subject_id = args["subject_id"]

        if args['mentee_id'] is not None:
            qry_history_subject.mentee_id = args['mentee_id']
        
        if args['score'] is not None:
            qry_history_subject.score = args['score']
            if int(args["score"]) >= 80:
                args["is_complete"] = True
            else:
                args["is_complete"] = False

            qry_history_subject.is_complete = args['is_complete']

        db.session.commit()

        return marshal(qry_history_subject, HistoriesSubject.response_fields), 200

    #endpoint for delete history subject by id
    def delete(self, id):
        qry_history_subject = HistoriesSubject.query.get(id)
        
        if qry_history_subject is not None:
            db.session.delete(qry_history_subject)
            db.session.commit()

            return {"status": "DELETED SUCCESS"}, 200
        
        return {"status": "ID NOT FOUND"}, 200


class HistoriesSubjectAll(Resource):
    #endpoint to get all and sort by score and created at
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=("score", "created_at"))
        parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry_history_subject = HistoriesSubject.query

        if args["orderby"] is not None:
            if args['orderby'] == "score":
                if args["sort"] == "desc":
                    qry_history_subject = qry_history_subject.order_by(desc(HistoriesSubject.score))
                else:
                    qry_history_subject = qry_history_subject.order_by(HistoriesSubject.score)
            if args['orderby'] == "created_at":
                if args["sort"] == "desc":
                    qry_history_subject = qry_history_subject.order_by(desc(HistoriesSubject.created_at))
                else:
                    qry_history_subject = qry_history_subject.order_by(HistoriesSubject.created_at)

        rows = []
        for row in qry_history_subject.limit(args['rp']).offset(offset).all():
            if row.status == True:
                row = marshal(row, HistoriesSubject.response_fields)
                rows.append(row)

        return rows, 200


class HistoriesSubjectAllStatus(Resource):
    #endpoint to get all status of history subject
    def get(self):
        qry_history_subject = HistoriesSubject.query

        rows = []
        for row in qry_history_subject:
            row = marshal(row, HistoriesSubject.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200

api.add_resource(HistoriesSubjectAll, "")
api.add_resource(HistoriesSubjectResource, "", "/<id>")
api.add_resource(HistoriesSubjectAllStatus, "", "/all")