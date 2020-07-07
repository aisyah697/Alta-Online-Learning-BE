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
    verify_jwt_in_request,
    jwt_required,
    get_jwt_claims,
)
from blueprints import admin_required

import boto3

from .model import FilesSubject

bp_file_subject = Blueprint("file_subject", __name__)
api = Api(bp_file_subject)


class FilesSubjectResource(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for search file subject by id
    @admin_required
    def get(self, id=None):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            qry_file_subject = FilesSubject.query.filter_by(status=True).filter_by(id=id).first()

            if qry_file_subject is not None:
                return marshal(qry_file_subject, FilesSubject.response_fields), 200
            
            return {"status": "Id File Mentee not found"}, 404
        
        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    #endpoint for post file subject
    @admin_required
    def post(self):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
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
            content_file = args["content_file"]

            if content_file:
                randomstr = uuid.uuid4().hex
                filename_key = randomstr + "_" + content_file.filename
                filename_body = content_file

                # S3 Connect
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=app.config["ACCESS_KEY_ID"],
                    aws_secret_access_key=app.config["ACCESS_SECRET_KEY"]
                )

                # File Uploaded
                if args["category_file"] == "presentation":
                    s3.put_object(Bucket=app.config["BUCKET_NAME"], Key="presentation/"+filename_key, Body=filename_body, ACL='public-read')

                    filename = "https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/presentation/" + str(filename_key)
                    filename = filename.replace(" ", "+")

                elif args["category_file"] == "video":
                    s3.put_object(Bucket=app.config["BUCKET_NAME"], Key="video/"+filename_key, Body=filename_body, ACL='public-read')

                    filename = "https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/video/" + str(filename_key)
                    filename = filename.replace(" ", "+")
            
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

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    #endpoint for soft delete
    def put(self, id):
        #check id in query or not
        qry_file_subject = FilesSubject.query.get(id)
        
        if qry_file_subject is None:
            return {'status': 'File Mentee is NOT_FOUND'}, 404
        
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
    @admin_required
    def patch(self, id):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            #check id in querry or not
            qry_file_subject = FilesSubject.query.filter_by(status=True).filter_by(id=id).first()
            if qry_file_subject is None:
                return {'status': 'File Mentee is NOT_FOUND'}, 404

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

                    #remove avatar in storage
                    if qry_file_subject.category_file == "presentation":
                        filename = "presentation/"+filename.split("/")[-1]
                        filename = filename.replace("+", " ")
                    elif qry_file_subject.category_file == "video":
                        filename = "video/"+filename.split("/")[-1]
                        filename = filename.replace("+", " ")

                    # S3 Connect
                    s3 = boto3.client(
                        's3',
                        aws_access_key_id=app.config["ACCESS_KEY_ID"],
                        aws_secret_access_key=app.config["ACCESS_SECRET_KEY"]
                    )

                    s3.delete_object(Bucket=app.config["BUCKET_NAME"], Key=filename)

                    #Change content file subject in storage
                    content_file = args["content_file"]
                    
                    randomstr = uuid.uuid4().hex
                    filename_key = randomstr + "_" + content_file.filename
                    filename_body = content_file

                    # S3 Connect
                    s3 = boto3.client(
                        's3',
                        aws_access_key_id=app.config["ACCESS_KEY_ID"],
                        aws_secret_access_key=app.config["ACCESS_SECRET_KEY"]
                    )

                    # Image Uploaded
                    if args["category_file"] == "presentation":
                        s3.put_object(Bucket=app.config["BUCKET_NAME"], Key="presentation/"+filename_key, Body=filename_body, ACL='public-read')

                        filename = "https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/presentation/" + str(filename_key)
                        filename = filename.replace(" ", "+")

                    elif args["category_file"] == "video":
                        s3.put_object(Bucket=app.config["BUCKET_NAME"], Key="video/"+filename_key, Body=filename_body, ACL='public-read')

                        filename = "https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/video/" + str(filename_key)
                        filename = filename.replace(" ", "+")
        
                    qry_file_subject.content_file = filename

                else:
                    content_file = args["content_file"]
                    
                    randomstr = uuid.uuid4().hex
                    filename_key = randomstr + "_" + content_file.filename
                    filename_body = content_file

                    # S3 Connect
                    s3 = boto3.client(
                        's3',
                        aws_access_key_id=app.config["ACCESS_KEY_ID"],
                        aws_secret_access_key=app.config["ACCESS_SECRET_KEY"]
                    )

                    # Image Uploaded
                    if args["category_file"] == "presentation":
                        s3.put_object(Bucket=app.config["BUCKET_NAME"], Key="presentation/"+filename_key, Body=filename_body, ACL='public-read')

                        filename = "https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/presentation/" + str(filename_key)
                        filename = filename.replace(" ", "+")

                    elif args["category_file"] == "video":
                        s3.put_object(Bucket=app.config["BUCKET_NAME"], Key="video/"+filename_key, Body=filename_body, ACL='public-read')

                        filename = "https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/video/" + str(filename_key)
                        filename = filename.replace(" ", "+")
        
                    qry_file_subject.content_file = filename

            if args['category_file'] is not None:
                qry_file_subject.category_file = args["category_file"]
            
            db.session.commit()

            return marshal(qry_file_subject, FilesSubject.response_fields), 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    #Endpoint delete file subject by Id
    @admin_required
    def delete(self, id):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            qry_file_subject = FilesSubject.query.get(id)
            #Check content file subject in query
            if qry_file_subject is not None:
                filename = qry_file_subject.content_file

                #remove avatar in storage
                if qry_file_subject.category_file == "presentation":
                    filename = "presentation/"+filename.split("/")[-1]
                    filename = filename.replace("+", " ")
                elif qry_file_subject.category_file == "video":
                    filename = "video/"+filename.split("/")[-1]
                    filename = filename.replace("+", " ")

                # S3 Connect
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=app.config["ACCESS_KEY_ID"],
                    aws_secret_access_key=app.config["ACCESS_SECRET_KEY"]
                )
                
                s3.delete_object(Bucket=app.config["BUCKET_NAME"], Key=filename)
                
                db.session.delete(qry_file_subject)
                db.session.commit()

                return {"status": "DELETED SUCCESS"}, 200

            return {"status": "NOT_FOUND"}, 404

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class FilesSubjectAll(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint to get all and sort by subject_id and category_file
    @admin_required
    def get(self):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
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

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class FilesSubjectAllStatus(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200
        
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