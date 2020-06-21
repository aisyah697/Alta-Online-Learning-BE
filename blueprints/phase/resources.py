import json
import os
import werkzeug
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app
from sqlalchemy import desc
import hashlib, uuid
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
    get_jwt_claims,
)

from .model import Phases

bp_phase = Blueprint("phase", __name__)
api = Api(bp_phase)

class PhasesResource(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for get phases by ID
    def get(self, id=None):
        qry_phase = Phases.query.filter_by(status=True).filter_by(id=id).first()

        if qry_phase is not None:
            qry_phase = marshal(qry_phase, Phases.response_fields)

            return qry_phase, 200
        
        return {"status": "Id Phases is not found"}, 404

    #endpoint post phase
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", location="json", required=True)
        parser.add_argument("description", location="json")
        parser.add_argument("status", location="json", type=bool, default=True)
        args = parser.parse_args()

        result = Phases(
            args["name"],
            args["description"],
            args["status"]
        )

        db.session.add(result)
        db.session.commit()

        return marshal(result, Phases.response_fields), 200

    #endpoint for soft delete
    def put(self, id):
        #check id in query or not
        qry_phase = Phases.query.get(id)
        
        if qry_phase is None:
            return {'status': 'Phase is NOT_FOUND'}, 404
        
        #input update status for soft delete
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete      
        qry_phase.status = args['status']

        db.session.commit()

        return marshal(qry_phase, Phases.response_fields), 200
    
    #endpoint for edit phase
    def patch(self, id):
        #check id in query or not
        qry_phase = Phases.query.get(id)
        
        if qry_phase is None:
            return {'status': 'Phase is NOT_FOUND'}, 404
        
        #input update description phase
        parser = reqparse.RequestParser()
        parser.add_argument("description", location="json")
        args = parser.parse_args()
        
        #change description phase     
        if args['description'] is not None:
            qry_phase.description = args['description']

        db.session.commit()

        return marshal(qry_phase, Phases.response_fields), 200

    #Endpoint delete phase by Id
    def delete(self, id):
        qry_phase = Phases.query.get(id)

        if qry_phase is not None:
            db.session.delete(qry_phase)
            db.session.commit()

            return {"status": "DELETED SUCCESS"}, 200

        return {"status": "NOT_FOUND"}, 404


class PhasesAll(Resource):
    #endpoint to get all and sort by choice and created_at
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=("id", "created_at"))
        parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry_phase = Phases.query

        if args["orderby"] is not None:
            if args['orderby'] == "id":
                if args["sort"] == "desc":
                    qry_phase = qry_phase.order_by(desc(Phases.id))
                else:
                    qry_phase = qry_phase.order_by(Phases.id)
            elif args["orderby"] == "created_at":
                if args["sort"] == "desc":
                    qry_phase = qry_phase.order_by(desc(Phases.created_at))
                else:
                    qry_phase = qry_phase.order_by(Phases.created_at)

        rows = []
        for row in qry_phase.limit(args['rp']).offset(offset).all():
            if row.status == True:
                row = marshal(row, Phases.response_fields)
                rows.append(row)

        return rows, 200


class PhasesAllStatus(Resource):
    #endpoint to get all status of choice 
    def get(self):
        qry_phase = Phases.query

        rows = []
        for row in qry_phase:
            row = marshal(row, Phases.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200


api.add_resource(PhasesAll, "")
api.add_resource(PhasesResource, "", "/<id>")
api.add_resource(PhasesAllStatus, "", "/all")