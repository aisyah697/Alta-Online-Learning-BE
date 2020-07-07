import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app
from sqlalchemy import desc
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    verify_jwt_in_request,
    jwt_required,
    get_jwt_claims,
)
from blueprints import admin_required

from .model import Livecodes
from ..exam.model import Exams

bp_livecode = Blueprint("livecode", __name__)
api = Api(bp_livecode)


class LivecodesResource(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for get livecode by ID
    @admin_required
    def get(self, id=None):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            qry_livecode = Livecodes.query.filter_by(status=True).filter_by(id=id).first()

            if qry_livecode is not None:
                livecode = marshal(qry_livecode, Livecodes.response_fields)
                
                return livecode, 200
            
            return {"status": "Id livecode is not found"}, 404

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    #endpoint post livecode
    @admin_required
    def post(self):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            parser = reqparse.RequestParser()
            parser.add_argument("exam_id", location="json", required=True)
            parser.add_argument("name", location="json")
            parser.add_argument("description", location="json")
            parser.add_argument("link", location="json")
            parser.add_argument("status", location="json", type=bool, default=True)
            args = parser.parse_args()

            #check livecode is there in database or not
            qry_livecode = Livecodes.query.filter_by(exam_id=args["exam_id"]).first()

            if qry_livecode is not None:
                return {"status": "Livecode is already there for this subject"}

            #check exam_id that mentioned is in database or not
            qry_exam = Exams.query.filter_by(id=args["exam_id"]).first()

            if qry_exam is None:
                return {"status": "Exam isn't there in database"}, 404

            result = Livecodes(
                args["exam_id"],
                args["name"],
                args["description"],
                args["link"],
                args["status"]
            )

            db.session.add(result)
            db.session.commit()

            return marshal(result, Livecodes.response_fields), 200
        
        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    #endpoint for soft delete
    def put(self, id):
        #check id in query or not
        qry_livecode = Livecodes.query.get(id)
        
        if qry_livecode is None:
            return {'status': 'Livecode is NOT_FOUND'}, 404
        
        #input update status for soft delete
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete      
        qry_livecode.status = args['status']

        db.session.commit()

        return marshal(qry_livecode, Livecodes.response_fields), 200

    #endpoint for update livecode
    @admin_required
    def patch(self, id):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            qry_livecode = Livecodes.query.filter_by(status=True).filter_by(id=id).first()
            if qry_livecode is None:
                return {'status': 'Livecode is NOT_FOUND'}, 404

            parser = reqparse.RequestParser()
            parser.add_argument("exam_id", location="json")
            parser.add_argument("name", location="json")
            parser.add_argument("description", location="json")
            parser.add_argument("link", location="json")
            args = parser.parse_args()

            if args['exam_id'] is not None:
                qry_livecode.exam_id = args['exam_id']

            if args['name'] is not None:
                qry_livecode.name = args['name']

            if args['description'] is not None:
                qry_livecode.description = args['description']

            if args['link'] is not None:
                qry_livecode.link = args['link']

            db.session.commit()

            return marshal(qry_livecode, Livecodes.response_fields), 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    #Endpoint delete livecode by Id
    @admin_required
    def delete(self, id):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            livecode_exam = Livecodes.query.get(id)

            if livecode_exam is not None:
                db.session.delete(livecode_exam)
                db.session.commit()

                return {"status": "DELETED SUCCESS"}, 200

            return {"status": "NOT_FOUND"}, 404

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class LivecodesAll(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint to get all and sort by exam_id
    @admin_required
    def get(self):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=25)
            parser.add_argument('orderby', location='args', help='invalid status', choices=("exam_id"))
            parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']

            qry_livecode = Livecodes.query

            if args["orderby"] is not None:
                if args['orderby'] == "exam_id":
                    if args["sort"] == "desc":
                        qry_livecode = qry_livecode.order_by(desc(Livecodes.exam_id))
                    else:
                        qry_livecode = qry_livecode.order_by(Livecodes.exam_id)
                
            rows = []
            for row in qry_livecode.limit(args['rp']).offset(offset).all():
                if row.status == True:
                    row = marshal(row, Livecodes.response_fields)
                    rows.append(row)

            return rows, 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class LivecodesAllStatus(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint to get all status of livecode
    def get(self):
        qry_livecode = Livecodes.query

        rows = []
        for row in qry_livecode:
            row = marshal(row, Livecodes.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200


api.add_resource(LivecodesAll, "")
api.add_resource(LivecodesResource, "", "/<id>")
api.add_resource(LivecodesAllStatus, "", "/all")