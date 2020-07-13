import json
import os
import werkzeug
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app
from sqlalchemy import desc

from .model import RequirementsModule

bp_requirement_module = Blueprint("requirement_module", __name__)
api = Api(bp_requirement_module)


class RequirementsModuleResource(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for search requirement module by id
    def get(self, id=None):
        qry_requirement_module = RequirementsModule.query.filter_by(status=True).filter_by(id=id).first()

        if qry_requirement_module is not None:
            return marshal(qry_requirement_module, RequirementsModule.response_fields), 200
        
        return {"status": "Id Requirement Module not found"}, 404

    #endpoint for post requirement module
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("module_id", location="json", required=True)
        parser.add_argument("description", location="json")
        parser.add_argument("status", location="json", default=True, type=bool)
        args = parser.parse_args()

        result = RequirementsModule(
            args["module_id"],
            args["description"],
            args["status"]
        )

        db.session.add(result)
        db.session.commit()

        return marshal(result, RequirementsModule.response_fields), 200

    #endpoint for soft delete
    def put(self, id):
        #check id in querry or not
        qry_requirement_module = RequirementsModule.query.get(id)
        if qry_requirement_module is None:
            return {'status': 'Requirement Module is NOT_FOUND'}, 404

        #input update status 
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete
        qry_requirement_module.status = args["status"]

        db.session.commit()

        return marshal(qry_requirement_module, RequirementsModule.response_fields), 200

    #endpoint for update field
    def patch(self, id):        
        #check id in querry or not
        qry_requirement_module = RequirementsModule.query.filter_by(status=True).filter_by(id=id).first()
        if qry_requirement_module is None:
            return {'status': 'Requirement Module is NOT_FOUND'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument("description", location="json")
        args = parser.parse_args()

        if args['description'] is not None:
            qry_requirement_module.description = args["description"]

        db.session.commit()

        return marshal(qry_requirement_module, RequirementsModule.response_fields), 200

    #endpoint for delete requirement module by id
    def delete(self, id):
        qry_requirement_module = RequirementsModule.query.get(id)
        
        if qry_requirement_module is not None:
            db.session.delete(qry_requirement_module)
            db.session.commit()
            
            return {"status": "DELETED SUCCESS"}, 200
        
        return {"status": "ID NOT FOUND"}, 404


class RequirementsModuleAll(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint to get all and sort by modul_id
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=("module_id"))
        parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry_requirement_module = RequirementsModule.query

        if args["orderby"] is not None:
            if args['orderby'] == "module_id":
                if args["sort"] == "desc":
                    qry_requirement_module = qry_requirement_module.order_by(desc(RequirementsModule.module_id))
                else:
                    qry_requirement_module = qry_requirement_module.order_by(RequirementsModule.module_id)

        rows = []
        for row in qry_requirement_module.limit(args['rp']).offset(offset).all():
            if row.status == True:
                row = marshal(row, RequirementsModule.response_fields)
                rows.append(row)

        return rows, 200


class RequirementsModuleAllStatus(Resource):
    #endpoint to get all status of requirement module
    def get(self):
        qry_requirement_module = RequirementsModule.query

        rows = []
        for row in qry_requirement_module:
            row = marshal(row, RequirementsModule.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200

api.add_resource(RequirementsModuleAll, "")
api.add_resource(RequirementsModuleResource, "", "/<id>")
api.add_resource(RequirementsModuleAllStatus, "", "/all")