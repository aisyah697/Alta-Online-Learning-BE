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
from blueprints import mentee_required
from  sqlalchemy.sql.expression import func, select

from .model import Altatests
from ..detail_altatest.model import DetailsAltatest
from ..question_altatest.model import QuestionsAltatest
from ..choice_altatest.model import ChoicesAltatest

bp_altatest = Blueprint("altatest", __name__)
api = Api(bp_altatest)


class AltatestsResource(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for search altatest by id
    def get(self, id=None):
        qry_altatest = Altatests.query.filter_by(status=True).filter_by(id=id).first()

        if qry_altatest is not None:
            qry_detail_question = DetailsAltatest.query.filter_by(altatest_id=id).all()
            rows = []
            for question in qry_detail_question:
                arrays = []
                qry_choice = ChoicesAltatest.query.order_by(func.rand()).filter_by(question_id=question.question_id).all()
                for choice in qry_choice:
                    arrays.append(marshal(choice, ChoicesAltatest.response_fields))
                
                question_altatest = marshal(QuestionsAltatest.query.get(question.question_id), QuestionsAltatest.response_fields)
                question_altatest["choice"] = arrays

                rows.append(question_altatest)

            qry_altatest = marshal(qry_altatest, Altatests.response_fields)
            qry_altatest["question"] = rows

            return qry_altatest, 200
        
        return {"status": "Id Altatests not found"}, 404

    #endpoint post altatest
    @mentee_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool, default=True)
        parser.add_argument("question_sum", location="json", default=25)
        args = parser.parse_args()

        result = Altatests(
            args["question_sum"],
            args["status"]
        )

        db.session.add(result)
        db.session.commit()

        qry_question = QuestionsAltatest.query.order_by(func.rand()).limit(args["question_sum"])
        rows = []
        for question in qry_question:
            detail = DetailsAltatest(
                result.id, question.id, True
            )

            db.session.add(detail)
            db.session.commit()

            qry_choice = ChoicesAltatest.query.order_by(func.rand()).filter_by(question_id=question.id).all()
            
            question_altatest = marshal(question, QuestionsAltatest.response_fields)
            
            if qry_choice:
                arrays = []
                for choice in qry_choice:
                    arrays.append(marshal(choice, ChoicesAltatest.response_fields))

                question_altatest["choice"] = arrays
                
            rows.append(question_altatest)
        
        result = marshal(result, Altatests.response_fields)
        result["question"] = rows

        return result, 200

    #endpoint for soft delete
    def put(self, id):
        #check id in query or not
        qry_altatest = Altatests.query.get(id)
        
        if qry_altatest is None:
            return {'status': 'Altatest is NOT_FOUND'}, 404
        
        #input update status for soft delete 
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete      
        qry_altatest.status = args['status']

        db.session.commit()

        return marshal(qry_altatest, Altatests.response_fields), 200

    #Endpoint delete Altatest by Id
    @mentee_required
    def delete(self, id):
        qry_altatest = Altatests.query.get(id)

        if qry_altatest is not None:
            db.session.delete(qry_altatest)
            db.session.commit()

            return {"status": "DELETED SUCCESS"}, 200

        return {"status": "NOT_FOUND"}, 404


class AltatestAll(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint to get all and sort by choice and created_at
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=("question_sum", "created_at"))
        parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry_altatest = Altatests.query

        if args["orderby"] is not None:
            if args["orderby"] == "question_sum":
                if args["sort"] == "desc":
                    qry_altatest = qry_altatest.order_by(desc(Altatests.question_sum))
                else:
                    qry_altatest = qry_altatest.order_by(Altatests.question_sum)
            elif args["orderby"] == "created_at":
                if args["sort"] == "desc":
                    qry_altatest = qry_altatest.order_by(desc(Altatests.created_at))
                else:
                    qry_altatest = qry_altatest.order_by(Altatests.created_at)

        rows = []
        for row in qry_altatest.limit(args['rp']).offset(offset).all():
            if row.status == True:
                row = marshal(row, Altatests.response_fields)
                rows.append(row)

        return rows, 200


class AltatestAllStatus(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200
    
    #endpoint to get all status of altatest 
    def get(self):
        qry_altatest = Altatests.query

        rows = []
        for row in qry_altatest:
            row = marshal(row, Altatests.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200

api.add_resource(AltatestAll, "")
api.add_resource(AltatestsResource, "", "/<id>")
api.add_resource(AltatestAllStatus, "", "/all")