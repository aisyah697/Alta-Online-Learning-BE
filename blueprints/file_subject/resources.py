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

from .model import FilesSubject

bp_file_subject = Blueprint("file_subject", __name__)
api = Api(bp_file_subject)


class FilesSubjectResource(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for search file subject by id
    def get(self, id=None):
        qry_file_subject = FilesSubject.query.filter_by(status=True).filter_by(id=id).first()

        if qry_file_subject is not None:
            return marshal(qry_file_subject, FilesSubject.response_fields), 200
        
        return {"status": "Id File Subject not found"}, 404

    #endpoint for post file subject
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("subject_id", location="form", required=True)
        parser.add_argument("name", location="form")
        parser.add_argument("content_file", type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument("category_file", location="form", help='category file not available', choices=("presentation", "video"))
        parser.add_argument("status", location="form", default="True")
        args = parser.parse_args()

        #for status, status used to soft delete 
        if args["status"] == "True" or args["status"] == "true":
            args["status"] = True
        elif args["status"] == "False" or args["status"] == "false":
            args["status"] = False

        #for upload image in storage
        if args["category_file"] == "presentation":
            UPLOAD_FOLDER = app.config["UPLOAD_MEDIA_PRESENTATION"]
        elif args["category_file"] == "video":
            UPLOAD_FOLDER = app.config["UPLOAD_MEDIA_VIDEO"]

        content_file = args["content_file"]

        if content_file:
            randomstr = uuid.uuid4().hex
            filename = randomstr+"_"+content_file.filename
            content_file.save(os.path.join("."+UPLOAD_FOLDER, filename))
        else:
            filename = None

        result = FilesSubject(
            args["subject_id"],
            args["name"],
            filename,
            args["category_file"],
            args["status"]
        )

        db.session.add(result)
        db.session.commit()

        return marshal(result, FilesSubject.response_fields), 200

    #endpoint for soft delete
    def put(self, id):
        #check id in query or not
        qry_file_subject = FilesSubject.query.get(id)
        
        if qry_file_subject is None:
            return {'status': 'File Subject is NOT_FOUND'}, 404
        
        #input update status for soft delete
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="form")
        args = parser.parse_args()

        #for status, status used to soft delete 
        if args["status"] == "True" or args["status"] == "true":
            args["status"] = True
        elif args["status"] == "False" or args["status"] == "false":
            args["status"] = False
        
        #change status for soft delete      
        qry_file_subject.status = args['status']

        db.session.commit()

        return marshal(qry_file_subject, FilesSubject.response_fields), 200

    #endpoint for update field
    def patch(self, id):        
        #check id in querry or not
        qry_file_subject = FilesSubject.query.filter_by(status=True).filter_by(id=id).first()
        if qry_file_subject is None:
            return {'status': 'File Subject is NOT_FOUND'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument("subject_id", location="form")
        parser.add_argument("name", location="form")
        parser.add_argument("content_file", type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument("category_file", location="form", help='category file not available', choices=("presentation", "video"))
        args = parser.parse_args()

        if args['subject_id'] is not None:
            qry_file_subject.subject_id = args["subject_id"]
        
        if args['name'] is not None:
            qry_file_subject.name = args["name"]

        if args['content_file'] is not None:
            #Check content file subject in query
            if qry_file_subject.content_file is not None:
                filename = qry_file_subject.content_file

                #Remove content file subject in storage
                if qry_file_subject.category_file == "presentation":
                    UPLOAD_FOLDER = app.config["UPLOAD_MEDIA_PRESENTATION"]
                elif qry_file_subject.category_file == "video":
                    UPLOAD_FOLDER = app.config["UPLOAD_MEDIA_VIDEO"]
                
                os.remove(os.path.join("."+UPLOAD_FOLDER, filename))

                content_file = args["content_file"]
                
                #Change content file subject in storage
                if content_file:
                    if args["category_file"] == "presentation":
                        UPLOAD_FOLDER = app.config["UPLOAD_MEDIA_PRESENTATION"]
                    elif args["category_file"] == "video":
                        UPLOAD_FOLDER = app.config["UPLOAD_MEDIA_VIDEO"]

                    randomstr = uuid.uuid4().hex
                    filename = randomstr+"_"+content_file.filename
                    content_file.save(os.path.join("."+UPLOAD_FOLDER, filename))

                qry_file_subject.content_file = filename

            else:
                if args["category_file"] == "presentation":
                    UPLOAD_FOLDER = app.config["UPLOAD_MEDIA_PRESENTATION"]
                elif args["category_file"] == "video":
                    UPLOAD_FOLDER = app.config["UPLOAD_MEDIA_VIDEO"]

                content_file = args["content_file"]
                
                #Change content file subject in storage
                if content_file:
                    randomstr = uuid.uuid4().hex
                    filename = randomstr+"_"+content_file.filename
                    content_file.save(os.path.join("."+UPLOAD_FOLDER, filename))

                qry_file_subject.content_file = filename

        if args['category_file'] is not None:
            qry_file_subject.category_file = args["category_file"]
        
        db.session.commit()

        return marshal(qry_file_subject, FilesSubject.response_fields), 200

    #Endpoint delete file subject by Id
    def delete(self, id):        
        qry_file_subject = FilesSubject.query.get(id)
        filename = qry_file_subject.content_file

        if qry_file_subject is not None:
            UPLOAD_FOLDER = app.config["UPLOAD_MEDIA_VIDEO"]
            os.remove(os.path.join("."+UPLOAD_FOLDER, filename))
            
            db.session.delete(qry_file_subject)
            db.session.commit()

            return {"status": "DELETED SUCCESS"}, 200

        return {"status": "NOT_FOUND"}, 404


class FilesSubjectAll(Resource):
    #endpoint to get all and sort by subject_id and category_file
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=("subject_id", "category_file"))
        parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry_file_subject = FilesSubject.query

        if args["orderby"] is not None:
            if args['orderby'] == "subject_id":
                if args["sort"] == "desc":
                    qry_file_subject = qry_file_subject.order_by(desc(FilesSubject.subject_id))
                else:
                    qry_file_subject = qry_file_subject.order_by(FilesSubject.subject_id)
            elif args['orderby'] == "category_file":
                if args["sort"] == "desc":
                    qry_file_subject = qry_file_subject.order_by(desc(FilesSubject.category_file))
                else:
                    qry_file_subject = qry_file_subject.order_by(FilesSubject.category_file)

        rows = []
        for row in qry_file_subject.limit(args['rp']).offset(offset).all():
            if row.status == True:
                row = marshal(row, FilesSubject.response_fields)
                rows.append(row)

        return rows, 200


class FilesSubjectAllStatus(Resource):
    #endpoint to get all status of choice 
    def get(self):
        qry_file_subject = FilesSubject.query

        rows = []
        for row in qry_file_subject:
            row = marshal(row, FilesSubject.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200

api.add_resource(FilesSubjectAll, "")
api.add_resource(FilesSubjectResource, "", "/<id>")
api.add_resource(FilesSubjectAllStatus, "", "/all")