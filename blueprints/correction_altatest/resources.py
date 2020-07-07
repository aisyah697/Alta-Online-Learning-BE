import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app
from sqlalchemy import desc
from flask_jwt_extended import (
    JWTManager,
    get_jwt_identity,
    verify_jwt_in_request,
    jwt_required,
    get_jwt_claims,
)
from blueprints import mentee_required

from .model import CorrectionsAltatest
from ..history_altatest.model import HistoriesAltatest

bp_correction_altatest = Blueprint("correction_altatest", __name__)
api = Api(bp_correction_altatest)

class CorrectionsAltatestResource(Resource):
    # endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for show correction altatest
    @mentee_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("question_altatest_id", location="json", required=True)
        args = parser.parse_args()
        
        #get mentee_id from id authentification
        verify_jwt_in_request()
        claims = get_jwt_claims()

        #get history_altatest_id from mentee_id
        qry_history_altatest = HistoriesAltatest.query.filter_by(mentee_id=claims["id"]).first()

        qry_correction_altatest = CorrectionsAltatest.query.filter_by(status=True).filter_by(question_altatest_id=args["question_altatest_id"]).filter_by(history_altatest_id=qry_history_altatest.id).all()

        if qry_correction_altatest == []:
            return {"status": "Answer of this question is not found"}, 404

        return marshal(qry_correction_altatest, CorrectionsAltatest.response_fields), 200

    #Endpoint delete Correction Altatest by Id
    @mentee_required
    def delete(self, id):
        correction_altatest = CorrectionsAltatest.query.get(id)

        if correction_altatest is not None:
            db.session.delete(correction_altatest)
            db.session.commit()

            return {"status": "DELETED SUCCESS"}, 200

        return {"status": "NOT_FOUND"}, 404

api.add_resource(CorrectionsAltatestResource, "", "/<id>")