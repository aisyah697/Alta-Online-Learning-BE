import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app
from sqlalchemy import desc
import hashlib, uuid
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
    get_jwt_claims,
)

from blueprints.admin.model import Admins
from blueprints.mentee.model import Mentees


bp_auth = Blueprint("auth", __name__)
api = Api(bp_auth)


#Login for Admin
class AuthAdmin(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", location="json", required=True)
        parser.add_argument("password", location="json", required=True)
        args = parser.parse_args()

        qry_admin = Admins.query.filter_by(username=args["username"]).first()

        #Check There admin in table or not ?
        if qry_admin and qry_admin.status == True:
            username_salt = qry_admin.salt

            encoded = ("%s%s" % (args["password"], username_salt)).encode("utf-8")
            hash_pass = hashlib.sha512(encoded).hexdigest()

            #Check password correct or not
            if hash_pass == qry_admin.password:
                obj_username = marshal(qry_admin, Admins.response_fields)
                jwt_username = marshal(qry_admin, Admins.jwt_claims_fields)
                jwt_username["status"] = "admin"
                token = create_access_token(
                    identity=args["username"], user_claims=jwt_username
                )
                obj_username["token"] = token
                return obj_username, 200

            else:
                return {"status": "password wrong"}, 404
        
        else:
            return {"status": "username not registered"}, 404


#Login for Mentee
class AuthMentee(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", location="json", required=True)
        parser.add_argument("password", location="json", required=True)
        args = parser.parse_args()

        qry_mentee = Mentees.query.filter_by(username=args["username"]).first()

        #Check There mentee in table or not ?
        if qry_mentee and qry_mentee.status == True:
            username_salt = qry_mentee.salt

            encoded = ("%s%s" % (args["password"], username_salt)).encode("utf-8")
            hash_pass = hashlib.sha512(encoded).hexdigest()

            #Check password correct or not
            if hash_pass == qry_mentee.password:
                obj_username = marshal(qry_mentee, Mentees.response_fields)
                jwt_username = marshal(qry_mentee, Mentees.jwt_claims_fields)
                jwt_username["status"] = "mentee"
                token = create_access_token(
                    identity=args["username"], user_claims=jwt_username
                )
                obj_username["token"] = token
                return obj_username, 200

            else:
                return {"status": "password wrong"}, 404
        
        else:
            return {"status": "username not registered"}, 404


api.add_resource(AuthAdmin, "", "/admin")
api.add_resource(AuthMentee, "", "/mentee")