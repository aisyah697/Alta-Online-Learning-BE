import json
import os
import werkzeug
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from blueprints import db, app
from sqlalchemy import desc
import hashlib, uuid 
# from flask_jwt_extended import (
#     JWTManager,
#     create_access_token,
#     get_jwt_identity,
#     jwt_required,
#     get_jwt_claims,
# )

from .model import HistoriesPhase
from ..mentee.model import Mentees
from ..phase.model import Phases

bp_history_phase = Blueprint("history_phase", __name__)
api = Api(bp_history_phase)


class HistoriesPhaseResource(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for search history phase by id
    def get(self, id=None):
        qry_history_phase = HistoriesPhase.query.filter_by(status=True).filter_by(id=id).first()

        if qry_history_phase is not None:
            return marshal(qry_history_phase, HistoriesPhase.response_fields), 200
        
        return {"status": "Id history phase not found"}, 404

    #endpoint for post history phase
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("phase_id", location="json", required=True)
        parser.add_argument("mentee_id", location="json", required=True)
        parser.add_argument("score", location="json")
        parser.add_argument("certificate", location="json")
        parser.add_argument("status", location="json", type=bool, default=True)
        args = parser.parse_args()

        #Check phase and mentee is existance in database
        qry_history_phase = HistoriesPhase.query.filter_by(phase_id=args["phase_id"]).filter_by(mentee_id=args["mentee_id"]).filter_by(status=True).all()
        if len(qry_history_phase) > 0:
            return {"status": "Phase and Mentee is already there"}, 404

        #Check Id Mentee is in database or not
        qry_mentee = Mentees.query.get(args["mentee_id"])
        if qry_mentee is None:
            return {"status": "ID Mentee is Not Found"}, 404

        #Check Id Phase is in database or not
        qry_phase = Phases.query.get(args["phase_id"])
        if qry_phase is None:
            return {"status": "ID Phase is Not Found"}, 404

        #Make number certificate
        if int(args["score"]) >= 80:
            encoded = uuid.uuid4().hex
        else:
            encoded = None

        result = HistoriesPhase(
            args["phase_id"],
            args["mentee_id"],
            args["score"],
            encoded,
            args["status"]
        )

        db.session.add(result)
        db.session.commit()

        return marshal(result, HistoriesPhase.response_fields), 200

    #endpoint for soft delete
    def put(self, id):
        #check id in query or not
        qry_history_phase = HistoriesPhase.query.get(id)
        if qry_history_phase is None:
            return {'status': 'History Phase is NOT_FOUND'}, 404

        #input update status 
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete
        if args['status'] is not None:
            qry_history_phase.status = args['status']

        db.session.commit()

        return marshal(qry_history_phase, HistoriesPhase.response_fields), 200

    #endpoint for update field
    def patch(self, id):
        qry_history_phase = HistoriesPhase.query.filter_by(status=True).filter_by(id=id).first()
        if qry_history_phase is None:
            return {'status': 'History Phase is NOT_FOUND'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument("phase_id", location="json")
        parser.add_argument("mentee_id", location="json")
        parser.add_argument("score", location="json")
        parser.add_argument("certificate", location="json", type=bool, default=False)
        args = parser.parse_args()

        if args['phase_id'] is not None:
            qry_history_phase.phase_id = args["phase_id"]

        if args['mentee_id'] is not None:
            qry_history_phase.mentee_id = args['mentee_id']
        
        if args['score'] is not None:
            qry_history_phase.score = args['score']

        #Make number certificate
        if int(args["score"]) >= 80:
            print("test ========", qry_history_phase.certificate)
            if qry_history_phase.certificate is None:
                encoded = uuid.uuid4().hex
                qry_history_phase.certificate = encoded
        else:
            qry_history_phase.certificate = None

        db.session.commit()

        return marshal(qry_history_phase, HistoriesPhase.response_fields), 200

    #endpoint for delete history phase by id
    def delete(self, id):
        qry_history_phase = HistoriesPhase.query.get(id)
        
        if qry_history_phase is not None:
            db.session.delete(qry_history_phase)
            db.session.commit()

            return {"status": "DELETED SUCCESS"}, 200
        
        return {"status": "ID NOT FOUND"}, 200


class HistoriesPhaseAll(Resource):
    #endpoint to get all and sort by score and created at
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=("score", "created_at"))
        parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry_history_phase = HistoriesPhase.query

        if args["orderby"] is not None:
            if args['orderby'] == "score":
                if args["sort"] == "desc":
                    qry_history_phase = qry_history_phase.order_by(desc(HistoriesPhase.score))
                else:
                    qry_history_phase = qry_history_phase.order_by(HistoriesPhase.score)
            if args['orderby'] == "created_at":
                if args["sort"] == "desc":
                    qry_history_phase = qry_history_phase.order_by(desc(HistoriesPhase.created_at))
                else:
                    qry_history_phase = qry_history_phase.order_by(HistoriesPhase.created_at)

        rows = []
        for row in qry_history_phase.limit(args['rp']).offset(offset).all():
            if row.status == True:
                row = marshal(row, HistoriesPhase.response_fields)
                rows.append(row)

        return rows, 200


class HistoriesPhaseAllStatus(Resource):
    #endpoint to get all status of history phase
    def get(self):
        qry_history_phase = HistoriesPhase.query

        rows = []
        for row in qry_history_phase:
            row = marshal(row, HistoriesPhase.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200

api.add_resource(HistoriesPhaseAll, "")
api.add_resource(HistoriesPhaseResource, "", "/<id>")
api.add_resource(HistoriesPhaseAllStatus, "", "/all")