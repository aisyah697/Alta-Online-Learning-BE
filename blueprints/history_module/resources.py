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

from .model import HistoriesModule
from ..mentee.model import Mentees
from ..module.model import Modules

bp_history_module = Blueprint("history_module", __name__)
api = Api(bp_history_module)


class HistoriesModuleResource(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for search history module by id
    def get(self, id=None):
        qry_history_module = HistoriesModule.query.filter_by(status=True).filter_by(id=id).first()

        if qry_history_module is not None:
            return marshal(qry_history_module, HistoriesModule.response_fields), 200
        
        return {"status": "Id history module not found"}, 404

    #endpoint for post history module
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("module_id", location="json", required=True)
        parser.add_argument("mentee_id", location="json", required=True)
        parser.add_argument("score", location="json")
        parser.add_argument("is_complete", location="json", type=bool, default=False)
        parser.add_argument("status", location="json", type=bool, default=True)
        args = parser.parse_args()

        #Check module and mentee is existance in database
        qry_history_module = HistoriesModule.query.filter_by(module_id=args["module_id"]).filter_by(mentee_id=args["mentee_id"]).filter_by(status=True).all()
        if len(qry_history_module) > 0:
            return {"status": "Module and Mentee is already there"}, 404

        #Check Id Mentee is in database or not
        qry_mentee = Mentees.query.get(args["mentee_id"])
        if qry_mentee is None:
            return {"status": "ID Mentee is Not Found"}, 404

        #Check Id Module is in database or not
        qry_module = Modules.query.get(args["module_id"])
        if qry_module is None:
            return {"status": "ID Module is Not Found"}, 404

        result = HistoriesModule(
            args["module_id"],
            args["mentee_id"],
            args["score"],
            args["is_complete"],
            args["status"]
        )

        db.session.add(result)
        db.session.commit()

        return marshal(result, HistoriesModule.response_fields), 200

    #endpoint for soft delete
    def put(self, id):
        #check id in query or not
        qry_history_module = HistoriesModule.query.get(id)
        if qry_history_module is None:
            return {'status': 'History Module is NOT_FOUND'}, 404

        #input update status 
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete
        if args['status'] is not None:
            qry_history_module.status = args['status']

        db.session.commit()

        return marshal(qry_history_module, HistoriesModule.response_fields), 200

    #endpoint for update field
    def patch(self, id):
        qry_history_module = HistoriesModule.query.filter_by(status=True).filter_by(id=id).first()
        if qry_history_module is None:
            return {'status': 'History Module is NOT_FOUND'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument("module_id", location="json")
        parser.add_argument("mentee_id", location="json")
        parser.add_argument("score", location="json")
        parser.add_argument("is_complete", location="json", type=bool, default=False)
        args = parser.parse_args()

        if args['module_id'] is not None:
            qry_history_module.module_id = args["module_id"]

        if args['mentee_id'] is not None:
            qry_history_module.mentee_id = args['mentee_id']
        
        if args['score'] is not None:
            qry_history_module.score = args['score']

        if args['is_complete'] is not None:
            qry_history_module.is_complete = args['is_complete']

        db.session.commit()

        return marshal(qry_history_module, HistoriesModule.response_fields), 200

    #endpoint for delete history module by id
    def delete(self, id):
        qry_history_module = HistoriesModule.query.get(id)
        
        if qry_history_module is not None:
            db.session.delete(qry_history_module)
            db.session.commit()

            return {"status": "DELETED SUCCESS"}, 200
        
        return {"status": "ID NOT FOUND"}, 200


class HistoriesModuleAll(Resource):
    #endpoint to get all and sort by score and created at
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=("score", "created_at"))
        parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry_history_module = HistoriesModule.query

        if args["orderby"] is not None:
            if args['orderby'] == "score":
                if args["sort"] == "desc":
                    qry_history_module = qry_history_module.order_by(desc(HistoriesModule.score))
                else:
                    qry_history_module = qry_history_module.order_by(HistoriesModule.score)
            if args['orderby'] == "created_at":
                if args["sort"] == "desc":
                    qry_history_module = qry_history_module.order_by(desc(HistoriesModule.created_at))
                else:
                    qry_history_module = qry_history_module.order_by(HistoriesModule.created_at)

        rows = []
        for row in qry_history_module.limit(args['rp']).offset(offset).all():
            if row.status == True:
                row = marshal(row, HistoriesModule.response_fields)
                rows.append(row)

        return rows, 200


class HistoriesModuleAllStatus(Resource):
    #endpoint to get all status of history subject
    def get(self):
        qry_history_module = HistoriesModule.query

        rows = []
        for row in qry_history_module:
            row = marshal(row, HistoriesModule.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200

api.add_resource(HistoriesModuleAll, "")
api.add_resource(HistoriesModuleResource, "", "/<id>")
api.add_resource(HistoriesModuleAllStatus, "", "/all")