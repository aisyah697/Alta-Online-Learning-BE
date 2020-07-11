import json
import os
import werkzeug
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
from blueprints import admin_required

from .model import ChoicesAltatest
from ..question_altatest.model import QuestionsAltatest
from ..admin.model import Admins

bp_choice_altatest = Blueprint("choice_altatest", __name__)
api = Api(bp_choice_altatest)


class ChoicesAltatestResource(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for get choices by ID
    def get(self, id=None):
        qry_choice_altatest = ChoicesAltatest.query.filter_by(status=True).filter_by(id=id).first()

        if qry_choice_altatest is not None:
            choice_altatest = marshal(qry_choice_altatest, ChoicesAltatest.response_fields)
            
            return choice_altatest, 200
        
        return {"status": "Id Choice Altatest is not found"}, 404

    #endpoint post choice altatest
    @admin_required
    def post(self):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "council" or claims["role"] == "academic":
            parser = reqparse.RequestParser()
            parser.add_argument("question_id", location="json", required=True)
            parser.add_argument("choice", location="json", required=True)
            parser.add_argument("is_correct", location="json", type=bool, default=False)
            parser.add_argument("status", location="json", type=bool, default=True)
            args = parser.parse_args()

            qry_question_altatest = QuestionsAltatest.query.get(args["question_id"])
            question_altatest = marshal(qry_question_altatest, QuestionsAltatest.response_fields)
            if qry_question_altatest is None:
                return {"status": "Question for this choice is Not Found"}, 404

            result = ChoicesAltatest(
                args["question_id"],
                args["choice"],
                args["is_correct"],
                args["status"]
            )

            db.session.add(result)
            db.session.commit()

            return marshal(result, ChoicesAltatest.response_fields), 200

        else:
            return {"status": "admin isn't at role super, council, and academic admin"}, 404

    #endpoint for soft delete
    def put(self, id):
        #check id in query or not
        qry_choice_altatest = ChoicesAltatest.query.get(id)
        
        if qry_choice_altatest is None:
            return {'status': 'Choice Altatest is NOT_FOUND'}, 404
        
        #input update status for soft delete
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete      
        qry_choice_altatest.status = args['status']

        db.session.commit()

        return marshal(qry_choice_altatest, ChoicesAltatest.response_fields), 200

    #endpoint for update choice
    @admin_required
    def patch(self, id):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "council" or claims["role"] == "academic":
            qry_choice_altatest = ChoicesAltatest.query.filter_by(status=True).filter_by(id=id).first()
            if qry_choice_altatest is None:
                return {'status': 'Choice Altatest is NOT_FOUND'}, 404

            parser = reqparse.RequestParser()
            parser.add_argument("choice", location="json")
            parser.add_argument("is_correct", location="json", type=bool)
            args = parser.parse_args()

            if args['choice'] is not None:
                qry_choice_altatest.choice = args['choice']

            if args['is_correct'] is not None:
                qry_choice_altatest.is_correct = args['is_correct']

            db.session.commit()

            return marshal(qry_choice_altatest, ChoicesAltatest.response_fields), 200

        else:
            return {"status": "admin isn't at role super, council, and academic admin"}, 404

    #Endpoint delete choice Altatest by Id
    @admin_required
    def delete(self, id):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "council" or claims["role"] == "academic":
            choice_altatest = ChoicesAltatest.query.get(id)

            if choice_altatest is not None:
                db.session.delete(choice_altatest)
                db.session.commit()

                return {"status": "DELETED SUCCESS"}, 200

            return {"status": "NOT_FOUND"}, 404

        else:
            return {"status": "admin isn't at role super, council, and academic admin"}, 404


class ChoicesAltatestAll(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint to get all and sort by choice and created_at
    @admin_required
    def get(self):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "council" or claims["role"] == "academic":
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=25)
            parser.add_argument('orderby', location='args', help='invalid status', choices=("choice", "created_at"))
            parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']

            qry_choice_altatest = ChoicesAltatest.query

            if args["orderby"] is not None:
                if args['orderby'] == "choice":
                    if args["sort"] == "desc":
                        qry_choice_altatest = qry_choice_altatest.order_by(desc(ChoicesAltatest.choice))
                    else:
                        qry_choice_altatest = qry_choice_altatest.order_by(ChoicesAltatest.choice)
                elif args["orderby"] == "created_at":
                    if args["sort"] == "desc":
                        qry_choice_altatest = qry_choice_altatest.order_by(desc(ChoicesAltatest.created_at))
                    else:
                        qry_choice_altatest = qry_choice_altatest.order_by(ChoicesAltatest.created_at)

            rows = []
            for row in qry_choice_altatest.limit(args['rp']).offset(offset).all():
                if row.status == True:
                    row = marshal(row, ChoicesAltatest.response_fields)
                    rows.append(row)

            return rows, 200

        else:
            return {"status": "admin isn't at role super, council, and academic admin"}, 404


class ChoicesAltatestAllStatus(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200
        
    #endpoint to get all status of choice 
    def get(self):
        qry_choice_altatest = ChoicesAltatest.query

        rows = []
        for row in qry_choice_altatest:
            row = marshal(row, ChoicesAltatest.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200


api.add_resource(ChoicesAltatestAll, "")
api.add_resource(ChoicesAltatestResource, "", "/<id>")
api.add_resource(ChoicesAltatestAllStatus, "", "/all")