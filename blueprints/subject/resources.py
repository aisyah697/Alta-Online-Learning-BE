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

from .model import Subjects

bp_subject = Blueprint("subject", __name__)
api = Api(bp_subject)


class SubjectsResource(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for search subject by id
    def get(self, id=None):
        qry_subject = Subjects.query.filter_by(status=True).filter_by(id=id).first()

        if qry_subject is not None:
            return marshal(qry_subject, Subjects.response_fields), 200
        
        return {"status": "Id Mentee not found"}, 404

    #endpoint for post subject
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("module_id", location="json", required=True)
        parser.add_argument("name", location="json")
        parser.add_argument("description", location="json")
        parser.add_argument("quesioner", location="json")
        parser.add_argument("status", location="json", default=True, type=bool)
        args = parser.parse_args()

        result = Subjects(
            args["module_id"],
            args["name"],
            args["description"],
            args["quesioner"],
            args["status"]
        )

        db.session.add(result)
        db.session.commit()

        return marshal(result, Subjects.response_fields), 200

    #endpoint for soft delete
    def put(self, id):
        #check id in query or not
        qry_subject = Subjects.query.get(id)
        if qry_subject is None:
            return {'status': 'Mentee is NOT_FOUND'}, 404

        #input update status 
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete
        qry_subject.status = args["status"]

        db.session.commit()

        return marshal(qry_subject, Subjects.response_fields), 200

    #endpoint for update field
    def patch(self, id):        
        #check id in querry or not
        qry_subject = Subjects.query.filter_by(status=True).filter_by(id=id).first()
        if qry_subject is None:
            return {'status': 'Mentee is NOT_FOUND'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument("name", location="json")
        parser.add_argument("description", location="json")
        parser.add_argument("quesioner", location="json")
        args = parser.parse_args()

        if args['name'] is not None:
            qry_subject.description = args["name"]
        
        if args['description'] is not None:
            qry_subject.description = args["description"]
        
        if args['quesioner'] is not None:
            qry_subject.quesioner = args["quesioner"]

        db.session.commit()

        return marshal(qry_subject, Subjects.response_fields), 200

    #endpoint for delete subject by id
    def delete(self, id):
        qry_subject = Subjects.query.get(id)
        
        if qry_subject is not None:
            db.session.delete(qry_subject)
            db.session.commit()
            
            return {"status": "DELETED SUCCESS"}, 200
        
        return {"status": "ID NOT FOUND"}, 404


class SubjectsAll(Resource):
    #endpoint to get all and sort by name & modul_id
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=("name", "module_id"))
        parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry_subject = Subjects.query

        if args["orderby"] is not None:
            if args['orderby'] == "name":
                if args["sort"] == "desc":
                    qry_subject = qry_subject.order_by(desc(Subjects.name))
                else:
                    qry_subject = qry_subject.order_by(Subjects.name)
            elif args['orderby'] == "module_id":
                if args["sort"] == "desc":
                    qry_subject = qry_subject.order_by(desc(Subjects.module_id))
                else:
                    qry_subject = qry_subject.order_by(Subjects.module_id)

        rows = []
        for row in qry_subject.limit(args['rp']).offset(offset).all():
            if row.status == True:
                row = marshal(row, Subjects.response_fields)
                rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200


class SubjectsAllStatus(Resource):
    #endpoint to get all status of subject
    def get(self):
        qry_subject = Subjects.query

        rows = []
        for row in qry_subject:
            row = marshal(row, Subjects.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200

api.add_resource(SubjectsAll, "")
api.add_resource(SubjectsResource, "", "/<id>")
api.add_resource(SubjectsAllStatus, "", "/all")