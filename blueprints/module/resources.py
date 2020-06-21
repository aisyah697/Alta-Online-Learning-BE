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

from .model import Modules

bp_module = Blueprint("module", __name__)
api = Api(bp_module)


class ModulesResource(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for search module by id
    def get(self, id=None):
        qry_module = Modules.query.filter_by(status=True).filter_by(id=id).first()

        if qry_module is not None:
            return marshal(qry_module, Modules.response_fields), 200
        
        return {"status": "Id Modules not found"}, 404

    #endpoint for post module
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("admin_id", location="form", required=True)
        parser.add_argument("phase_id", location="form", required=True)
        parser.add_argument("name", location="form")
        parser.add_argument("description", location="form")
        parser.add_argument("image", type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument("status", location="form", default="True")
        args = parser.parse_args()

        #for status, status used to soft delete 
        if args["status"] == "True" or args["status"] == "true":
            args["status"] = True
        elif args["status"] == "False" or args["status"] == "false":
            args["status"] = False

        #for upload image in storage
        UPLOAD_FOLDER = app.config["UPLOAD_MEDIA_AVATAR"]

        module_image = args["image"]

        if module_image:
            randomstr = uuid.uuid4().hex
            filename = randomstr+"_"+module_image.filename
            module_image.save(os.path.join("."+UPLOAD_FOLDER, filename))
        else:
            filename = None

        result = Modules(
            args["admin_id"],
            args["phase_id"],
            args["name"],
            args["description"],
            filename,
            args["status"]
        )

        db.session.add(result)
        db.session.commit()

        return marshal(result, Modules.response_fields), 200

    #endpoint for soft delete
    def put(self, id):
        #check id in querry or not
        qry_module = Modules.query.get(id)
        if qry_module is None:
            return {'status': 'Module is NOT_FOUND'}, 404

        #input update status 
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="form")
        args = parser.parse_args()
        
        #change status for soft delete
        if args['status'] is not None:
            if args["status"] == "True" or args["status"] == "true":
                args["status"] = True
            elif args["status"] == "False" or args["status"] == "false":
                args["status"] = False
            
            qry_module.status = args['status']
        else:
            return {"status": "NOT FILLED"}, 404

        db.session.commit()

        return marshal(qry_module, Modules.response_fields), 200

    #endpoint for update field
    def patch(self, id):
        qry_module = Modules.query.filter_by(status=True).filter_by(id=id).first()
        if qry_module is None:
            return {'status': 'Module is NOT_FOUND'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument("admin_id", location="form")
        parser.add_argument("phase_id", location="form")
        parser.add_argument("name", location="form")
        parser.add_argument("description", location="form")
        parser.add_argument("image", type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()

        if args['admin_id'] is not None:
            qry_module.admin_id = args["admin_id"]

        if args['phase_id'] is not None:
            qry_module.phase_id = args['phase_id']
        
        if args['name'] is not None:
            qry_module.name = args['name']

        if args['description'] is not None:
            qry_module.description = args['description']

        if args['image'] is not None:
            #Check image in query
            if qry_module.image is not None:
                filename = qry_module.image

                #Remove image in storage
                UPLOAD_FOLDER = app.config["UPLOAD_MEDIA_AVATAR"]
                os.remove(os.path.join("."+UPLOAD_FOLDER, filename))

                module_image = args["image"]
                
                #Change image in storage
                if module_image:
                    randomstr = uuid.uuid4().hex
                    filename = randomstr+"_"+module_image.filename
                    module_image.save(os.path.join("."+UPLOAD_FOLDER, filename))

                qry_module.image = filename

            else:
                UPLOAD_FOLDER = app.config["UPLOAD_MEDIA_AVATAR"]

                module_image = args["image"]
                
                #Change image in storage
                if module_image:
                    randomstr = uuid.uuid4().hex
                    filename = randomstr+"_"+module_image.filename
                    module_image.save(os.path.join("."+UPLOAD_FOLDER, filename))

                qry_module.image = filename

        db.session.commit()

        return marshal(qry_module, Modules.response_fields), 200

    #endpoint for delete module by id
    def delete(self, id):
        qry_module = Modules.query.get(id)
        filename = qry_module.image
        
        if qry_module is not None:
            UPLOAD_FOLDER = app.config["UPLOAD_MEDIA_AVATAR"]
            os.remove(os.path.join("."+UPLOAD_FOLDER, filename))

            db.session.delete(qry_module)
            db.session.commit()
            return {"status": "DELETED SUCCESS"}, 200
        
        return {"status": "ID NOT FOUND"}, 200


class ModulesAll(Resource):
    #endpoint to get all and sort by admin_id, phase_id and name
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=("admin_id", "phase_id", "name"))
        parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry_module = Modules.query

        if args["orderby"] is not None:
            if args['orderby'] == "admin_id":
                if args["sort"] == "desc":
                    qry_module = qry_module.order_by(desc(Modules.admin_id))
                else:
                    qry_module = qry_module.order_by(Modules.admin_id)
            elif args["orderby"] == "phase_id":
                if args["sort"] == "desc":
                    qry_module = qry_module.order_by(desc(Modules.phase_id))
                else:
                    qry_module = qry_module.order_by(Modules.phase_id)
            elif args["orderby"] == 'name':
                if args["sort"] == "desc":
                    qry_module = qry_module.order_by(desc(Modules.name))
                else:
                    qry_module = qry_module.order_by(Modules.name)

        rows = []
        for row in qry_module.limit(args['rp']).offset(offset).all():
            if row.status == True:
                row = marshal(row, Modules.response_fields)
                rows.append(row)

        return rows, 200


class ModulesAllStatus(Resource):
    #endpoint to get all status of module
    def get(self):
        qry_module = Modules.query

        rows = []
        for row in qry_module:
            row = marshal(row, Modules.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200

api.add_resource(ModulesAll, "")
api.add_resource(ModulesResource, "", "/<id>")
api.add_resource(ModulesAllStatus, "", "/all")