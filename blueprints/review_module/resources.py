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

from .model import ReviewsModule
from ..mentee.model import Mentees

bp_review_module = Blueprint("review_module", __name__)
api = Api(bp_review_module)


class ReviewsModuleResource(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for search review module by id
    def get(self, id=None):
        qry_review_module = ReviewsModule.query.filter_by(status=True).filter_by(id=id).first()

        if qry_review_module is not None:
            return marshal(qry_review_module, ReviewsModule.response_fields), 200
        
        return {"status": "Id Review Module not found"}, 404

    #endpoint for post review module
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("mentee_id", location="json", required=True)
        parser.add_argument("module_id", location="json", required=True)
        parser.add_argument("content", location="json")
        parser.add_argument("score", location="json", help='score just 1 to 5', choices=("1", "2", "3", "4", "5"))
        parser.add_argument("status", location="json", default=True, type=bool)
        args = parser.parse_args()

        #check there no review given from 1 mentee for 1 module, because 1 mentee just can give review for 1 module
        qry_review_module = ReviewsModule.query.filter_by(mentee_id=args["mentee_id"]).filter_by(module_id=args["module_id"]).all()
        if qry_review_module:
            return {"status": "This mentee already give review for the module"}, 404

        result = ReviewsModule(
            args["mentee_id"],
            args["module_id"],
            args["content"],
            args["score"],
            args["status"]
        )

        db.session.add(result)
        db.session.commit()

        return marshal(result, ReviewsModule.response_fields), 200

    #endpoint for soft delete
    def put(self, id):
        #check id in querry or not
        qry_review_module = ReviewsModule.query.get(id)
        if qry_review_module is None:
            return {'status': 'Review Module is NOT_FOUND'}, 404

        #input update status 
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete
        qry_review_module.status = args["status"]

        db.session.commit()

        return marshal(qry_review_module, ReviewsModule.response_fields), 200

    #endpoint for update field
    def patch(self, id):
        qry_review_module = ReviewsModule.query.filter_by(status=True).filter_by(id=id).first()
        if qry_review_module is None:
            return {'status': 'Review Module is NOT_FOUND'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument("mentee_id", location="json")
        parser.add_argument("module_id", location="json")
        parser.add_argument("content", location="json")
        parser.add_argument("score", location="json", help='invalid status', choices=("1", "2", "3", "4", "5"))
        args = parser.parse_args()

        if args['mentee_id'] is not None:
            qry_review_module.mentee_id = args["mentee_id"]

        if args['module_id'] is not None:
            qry_review_module.module_id = args['module_id']
        
        if args['content'] is not None:
            qry_review_module.content = args['content']

        if args['score'] is not None:
            qry_review_module.score = args['score']

        db.session.commit()

        return marshal(qry_review_module, ReviewsModule.response_fields), 200

    #endpoint for delete review module by id
    def delete(self, id):
        qry_review_module = ReviewsModule.query.get(id)
        
        if qry_review_module is not None:
            db.session.delete(qry_review_module)
            db.session.commit()
            
            return {"status": "DELETED SUCCESS"}, 200
        
        return {"status": "ID NOT FOUND"}, 200


class ReviewsModuleAll(Resource):
    #endpoint to get all and sort by modul_id & score
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=("module_id", "score"))
        parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry_review_module = ReviewsModule.query

        if args["orderby"] is not None:
            if args['orderby'] == "module_id":
                if args["sort"] == "desc":
                    qry_review_module = qry_review_module.order_by(desc(ReviewsModule.module_id))
                else:
                    qry_review_module = qry_review_module.order_by(ReviewsModule.module_id)
            elif args['orderby'] == "score":
                if args["sort"] == "desc":
                    qry_review_module = qry_review_module.order_by(desc(ReviewsModule.score))
                else:
                    qry_review_module = qry_review_module.order_by(ReviewsModule.score)

        rows = []
        for row in qry_review_module.limit(args['rp']).offset(offset).all():
            if row.status == True:
                row = marshal(row, ReviewsModule.response_fields)
                rows.append(row)

        return rows, 200


class ReviewsModuleAllStatus(Resource):
    #endpoint to get all status of review module
    def get(self):
        qry_review_module = ReviewsModule.query

        rows = []
        for row in qry_review_module:
            row = marshal(row, ReviewsModule.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200

api.add_resource(ReviewsModuleAll, "")
api.add_resource(ReviewsModuleResource, "", "/<id>")
api.add_resource(ReviewsModuleAllStatus, "", "/all")