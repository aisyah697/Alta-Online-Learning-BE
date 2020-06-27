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

import re
import boto3

from .model import Admins

bp_admin = Blueprint("admin", __name__)
api = Api(bp_admin)


class AdminsResource(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for search admin by id
    def get(self, id=None):
        qry_admin = Admins.query.filter_by(status=True).filter_by(id=id).first()

        if qry_admin is not None:
            return marshal(qry_admin, Admins.response_fields), 200
        
        return {"status": "Id Admins not found"}, 404

    #endpoint for post admin
    @admin_required
    def post(self):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims["role"] == "super":
            parser = reqparse.RequestParser()
            parser.add_argument("username", location="form", required=True)
            parser.add_argument("password", location="form", required=True)
            parser.add_argument("full_name", location="form")
            parser.add_argument("role", location="form", required=True, help='invalid status', choices=('super', 'council', 'academic', 'bussiness'))
            parser.add_argument("email", location="form")
            parser.add_argument("address", location="form")
            parser.add_argument("phone", location="form")
            parser.add_argument("place_birth", location="form")
            parser.add_argument("date_birth", location="form")
            parser.add_argument("avatar", type=werkzeug.datastructures.FileStorage, location='files')
            parser.add_argument("github", location="form")
            parser.add_argument("description", location="form")
            parser.add_argument("status", location="form", default="True")
            args = parser.parse_args()

            #check username
            if len(args["username"]) < 6:
                return {"status": "username must be at least 6 character"}, 404

            #check phone number
            if args['phone'] is not None:
                phone = re.findall("^0[0-9]{7,14}", args["phone"])
                if phone == [] or phone[0] != str(args['phone']) or len(args["phone"]) > 15:
                    return {"status": "phone number not match"}, 404

            #check password
            if len(args["password"]) < 6:
                return {"status": "password must be 6 character"}, 404

            #check email
            if args['phone'] is not None:
                match=re.search("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", args["email"])
                if match is None:
                     return {"status": "your input of email is wrong"}, 404

            #for status, status used to soft delete
            if args["status"] == "True" or args["status"] == "true":
                args["status"] = True
            elif args["status"] == "False" or args["status"] == "false":
                args["status"] = False

            #for upload image in storage
            avatar = args["avatar"]

            if avatar:
                randomstr = uuid.uuid4().hex
                filename_key = randomstr + "_" + avatar.filename
                filename_body = avatar

                # S3 Connect
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=app.config["ACCESS_KEY_ID"],
                    aws_secret_access_key=app.config["ACCESS_SECRET_KEY"]
                )

                # Image Uploaded
                s3.put_object(Bucket=app.config["BUCKET_NAME"], Key="avatar/"+filename_key, Body=filename_body, ACL='public-read')

                filename = "https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/avatar/" + str(filename_key)
                filename = filename.replace(" ", "+")

            else:
                filename = None

            #for filled salt on field's table of admin
            salt = uuid.uuid4().hex
            encoded = ("%s%s" % (args["password"], salt)).encode("utf-8")
            hash_pass = hashlib.sha512(encoded).hexdigest()

            result = Admins(
                args["username"],
                hash_pass,
                args["full_name"],
                args["role"],
                args["email"],
                args["address"],
                args["phone"],
                args["place_birth"],
                args["date_birth"],
                filename,
                args["github"],
                args["description"],
                salt,
                args["status"]
            )

            db.session.add(result)
            db.session.commit()

            #for get token when register
            jwt_username = marshal(result, Admins.jwt_claims_fields)
            jwt_username["status"] = "admin"
            token = create_access_token(identity=args["username"], user_claims=jwt_username)

            #add key token in response of endpoint
            result = marshal(result, Admins.response_fields)
            result["token"] = token

            return result, 200
        
        else:
            return {"status": "admin isn't at role super admin"}, 404

    #endpoint for soft delete
    def put(self, id):
        #check id in querry or not
        qry_admin = Admins.query.get(id)
        if qry_admin is None:
            return {'status': 'Admin is NOT_FOUND'}, 404

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
            
            qry_admin.status = args['status']
        else:
            return {"status": "NOT FILLED"}, 404

        db.session.commit()

        return marshal(qry_admin, Admins.response_fields), 200

    #endpoint for update field
    def patch(self, id):
        qry_admin = Admins.query.filter_by(status=True).filter_by(id=id).first()
        if qry_admin is None:
            return {'status': 'Admin is NOT_FOUND'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument("username", location="form")
        parser.add_argument("password", location="form")
        parser.add_argument("full_name", location="form")
        parser.add_argument("role", location="form", help='invalid status', choices=('super', 'council', 'academic', 'bussiness'))
        parser.add_argument("email", location="form")
        parser.add_argument("address", location="form")
        parser.add_argument("phone", location="form")
        parser.add_argument("place_birth", location="form")
        parser.add_argument("date_birth", location="form")
        parser.add_argument("avatar", type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument("github", location="form")
        parser.add_argument("description", location="form")
        args = parser.parse_args()

        if args['username'] is not None:
            #check username
            if len(args["username"]) < 6:
                return {"status": "username must be at least 6 character"}, 404
            qry_admin.username = args['username']

        if args['password'] is not None:
            #cek password
            if len(args["password"]) < 6:
                return {"status": "password must be 6 character"}, 404
            encoded = ("%s%s" % (args["password"], qry_admin.salt)).encode("utf-8")
            hash_pass = hashlib.sha512(encoded).hexdigest()
            qry_admin.password = hash_pass

        if args['full_name'] is not None:
            qry_admin.full_name = args['full_name']
        
        if args['role'] is not None:
            qry_admin.role = args['role']

        if args['email'] is not None:
            #check email
            match=re.search("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", args["email"])
            if match is None:
                return {"status": "your input of email is wrong"}, 404
            qry_admin.email = args['email']

        if args['address'] is not None:
            qry_admin.address = args['address']

        if args['phone'] is not None:
            #cek phone number
            phone = re.findall("^0[0-9]{7,14}", args["phone"])
            if phone == [] or phone[0] != str(args['phone']) or len(args["phone"]) > 15:
                return {"status": "phone number not match"}, 404
            qry_admin.phone = args['phone']

        if args['place_birth'] is not None:
            qry_admin.place_birth = args['place_birth']

        if args['date_birth'] is not None:
            qry_admin.date_birth = args['date_birth']

        if args['avatar'] is not None:
            #Check avatar in query
            if qry_admin.avatar is not None:
                filename = qry_admin.avatar
                #remove avatar in storage
                filename = "avatar/"+filename.split("/")[-1]
                filename = filename.replace("+", " ")

                # S3 Connect
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=app.config["ACCESS_KEY_ID"],
                    aws_secret_access_key=app.config["ACCESS_SECRET_KEY"]
                )

                s3.delete_object(Bucket=app.config["BUCKET_NAME"], Key=filename)
 
                # #change avatar in storage
                avatar = args["avatar"]

                randomstr = uuid.uuid4().hex
                filename_key = randomstr + "_" + avatar.filename
                filename_body = avatar

                # S3 Connect
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=app.config["ACCESS_KEY_ID"],
                    aws_secret_access_key=app.config["ACCESS_SECRET_KEY"]
                )

                # Image Uploaded
                s3.put_object(Bucket=app.config["BUCKET_NAME"], Key="avatar/"+filename_key, Body=filename_body, ACL='public-read')

                filename = "https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/avatar/" + str(filename_key)
                filename = filename.replace(" ", "+")

                qry_admin.avatar = filename

            else:
                avatar = args["avatar"]

                randomstr = uuid.uuid4().hex
                filename_key = randomstr + "_" + avatar.filename
                filename_body = avatar

                # S3 Connect
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=app.config["ACCESS_KEY_ID"],
                    aws_secret_access_key=app.config["ACCESS_SECRET_KEY"]
                )

                # Image Uploaded
                s3.put_object(Bucket=app.config["BUCKET_NAME"], Key="avatar/"+filename_key, Body=filename_body, ACL='public-read')

                filename = "https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/avatar/" + str(filename_key)
                filename = filename.replace(" ", "+")

                qry_admin.avatar = filename

        if args['github'] is not None:
            qry_admin.github = args['github']

        if args['description'] is not None:
            qry_admin.description = args['description']

        db.session.commit()

        return marshal(qry_admin, Admins.response_fields), 200

    #endpoint for delete admin by id
    def delete(self, id):
        admin = Admins.query.get(id)
        filename = admin.avatar
        
        if admin is not None:
            if filename is not None:
                #remove avatar in storage
                filename = "avatar/"+filename.split("/")[-1]
                filename = filename.replace("+", " ")

                # S3 Connect
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=app.config["ACCESS_KEY_ID"],
                    aws_secret_access_key=app.config["ACCESS_SECRET_KEY"]
                )

                s3.delete_object(Bucket=app.config["BUCKET_NAME"], Key=filename)
            
            #remove database
            db.session.delete(admin)
            db.session.commit()
            return {"status": "DELETED SUCCESS"}, 200
        
        return {"status": "ID NOT FOUND"}, 200


class AdminsAll(Resource):
    #endpoint to get all and sort by username, full_name and role
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=("username", "full_name", "role"))
        parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry_admin = Admins.query

        if args["orderby"] is not None:
            if args['orderby'] == "username":
                if args["sort"] == "desc":
                    qry_admin = qry_admin.order_by(desc(Admins.username))
                else:
                    qry_admin = qry_admin.order_by(Admins.username)
            elif args["orderby"] == "full_name":
                if args["sort"] == "desc":
                    qry_admin = qry_admin.order_by(desc(Admins.full_name))
                else:
                    qry_admin = qry_admin.order_by(Admins.full_name)
            elif args["orderby"] == 'role':
                if args["sort"] == "desc":
                    qry_admin = qry_admin.order_by(desc(Admins.role))
                else:
                    qry_admin = qry_admin.order_by(Admins.role)

        rows = []
        for row in qry_admin.limit(args['rp']).offset(offset).all():
            if row.status == True:
                row = marshal(row, Admins.response_fields)
                rows.append(row)

        return rows, 200


class AdminsAllStatus(Resource):
    #endpoint to get all status of admin 
    def get(self):
        qry_admin = Admins.query

        rows = []
        for row in qry_admin:
            row = marshal(row, Admins.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200

api.add_resource(AdminsAll, "")
api.add_resource(AdminsResource, "", "/<id>")
api.add_resource(AdminsAllStatus, "", "/all")