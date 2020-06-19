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

from .model import HistoriesAltatest
from ..mentee.model import Mentees
from ..altatest.model import Altatests

bp_history_altatest = Blueprint("history_altatest", __name__)
api = Api(bp_history_altatest)


class HistoriesAltatestResource(Resource):
    # endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    # endpoint for get history altatest by ID
    def get(self, id=None):
        qry_history_altatest = HistoriesAltatest.query.filter_by(
            status=True).filter_by(id=id).first()

        if qry_history_altatest is not None:
            qry_history_altatest = marshal(
                qry_history_altatest, HistoriesAltatest.response_fields)

            return qry_history_altatest, 200

        return {"status": "Id History Altatest is not found"}, 404

    # endpoint post history altatest
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("altatest_id", location="json", required=True)
        parser.add_argument("mentee_id", location="json", required=True)
        parser.add_argument("score", location="json")
        parser.add_argument("status", location="json", type=bool, default=True)
        args = parser.parse_args()

        qry_altatest = Altatests.query.get(args["altatest_id"])
        qry_mentee = Mentees.query.get(args["mentee_id"])
        if qry_altatest is None:
            return {"status": "Altatest is Not Found"}, 404
        if qry_mentee is None:
            return {"status": "Mentee is Not Found"}, 404

        result = HistoriesAltatest(
            args["altatest_id"],
            args["mentee_id"],
            args["score"],
            args["status"]
        )

        db.session.add(result)
        db.session.commit()

        return marshal(result, HistoriesAltatest.response_fields), 200

    #endpoint for soft delete
    def put(self, id):
        #check id in query or not
        qry_history_altatest = HistoriesAltatest.query.get(id)
        
        if qry_history_altatest is None:
            return {'status': 'History Altatest is NOT_FOUND'}, 404
        
        #input update status for soft delete
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete      
        qry_history_altatest.status = args['status']

        db.session.commit()

        return marshal(qry_history_altatest, HistoriesAltatest.response_fields), 200

    #endpoint for change score
    def patch(self, id):
        #check id in query or not
        qry_history_altatest = HistoriesAltatest.query.get(id)
        
        if qry_history_altatest is None:
            return {'status': 'History Altatest is NOT_FOUND'}, 404
        
        #input update status for soft delete
        parser = reqparse.RequestParser()
        parser.add_argument("score", location="json")
        args = parser.parse_args()
        
        #change status for soft delete      
        if args['score'] is not None:
            qry_history_altatest.score = args['score']

        db.session.commit()

        return marshal(qry_history_altatest, HistoriesAltatest.response_fields), 200

    #Endpoint delete history Altatest by Id
    def delete(self, id):
        history_altatest = HistoriesAltatest.query.get(id)

        if history_altatest is not None:
            db.session.delete(history_altatest)
            db.session.commit()

            return {"status": "DELETED SUCCESS"}, 200

        return {"status": "NOT_FOUND"}, 404


class HistoriesAltatestAll(Resource):
    #endpoint to get all and sort by score and created_at
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=("score", "created_at"))
        parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry_history_altatest = HistoriesAltatest.query

        if args["orderby"] is not None:
            if args['orderby'] == "score":
                if args["sort"] == "desc":
                    qry_history_altatest = qry_history_altatest.order_by(desc(HistoriesAltatest.score))
                else:
                    qry_history_altatest = qry_history_altatest.order_by(HistoriesAltatest.score)
            elif args["orderby"] == "created_at":
                if args["sort"] == "desc":
                    qry_history_altatest = qry_history_altatest.order_by(desc(HistoriesAltatest.created_at))
                else:
                    qry_history_altatest = qry_history_altatest.order_by(HistoriesAltatest.created_at)

        rows = []
        for row in qry_history_altatest.limit(args['rp']).offset(offset).all():
            if row.status == True:
                row = marshal(row, HistoriesAltatest.response_fields)
                rows.append(row)

        return rows, 200

class HistoriesAltatestAllStatus(Resource):
    #endpoint to get all status of history altatest 
    def get(self):
        qry_history_altatest = HistoriesAltatest.query

        rows = []
        for row in qry_history_altatest:
            row = marshal(row, HistoriesAltatest.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200


api.add_resource(HistoriesAltatestAll, "")
api.add_resource(HistoriesAltatestResource, "", "/<id>")
api.add_resource(HistoriesAltatestAllStatus, "", "/all")
