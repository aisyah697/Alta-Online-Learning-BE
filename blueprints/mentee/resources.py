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
    jwt_required,
    get_jwt_claims,
)
from blueprints import admin_required, mentee_required

import boto3
import re

from .model import Mentees
from ..phase.model import Phases
from ..module.model import Modules
from ..subject.model import Subjects
from ..exam.model import Exams
from ..history_altatest.model import HistoriesAltatest
from ..history_phase.model import HistoriesPhase
from ..history_module.model import HistoriesModule
from ..history_subject.model import HistoriesSubject
from ..history_exam.model import HistoriesExam

bp_mentee = Blueprint("mentee", __name__)
api = Api(bp_mentee)


class MenteesResource(Resource):
    # For solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    # Endpoint for search mentee by id
    def get(self, id=None):
        qry_mentee = Mentees.query.filter_by(status=True).filter_by(id=id).first()

        if qry_mentee is not None:
            return marshal(qry_mentee, Mentees.response_fields), 200
        
        return {"status": "Id Mentees not found"}, 404

    # Endpoint for post mentee
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", location="form", required=True)
        parser.add_argument("password", location="form", required=True)
        parser.add_argument("full_name", location="form")
        parser.add_argument("email", location="form")
        parser.add_argument("address", location="form")
        parser.add_argument("phone", location="form")
        parser.add_argument("place_birth", location="form")
        parser.add_argument("date_birth", location="form")
        parser.add_argument("avatar", type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument("background_education", location="form")
        parser.add_argument("github", location="form")
        parser.add_argument("description", location="form")
        parser.add_argument("status", location="form", default="True")
        args = parser.parse_args()

        # Check existance username
        mentee = Mentees.query.filter_by(status=True).filter_by(username=args["username"]).first()
        if mentee is not None:
            return {"status": "username existance"}, 404

        # Check username
        if len(args["username"]) < 6:
            return {"status": "username must be at least 6 character"}, 404

        # Check phone number
        if args["phone"] is not None:
            phone = re.findall("^0[0-9]{7,14}", args["phone"])
            if phone == [] or phone[0] != str(args['phone']) or len(args["phone"]) > 15:
                return {"status": "phone number not match"}, 404

        # Check password
        if len(args["password"]) < 6:
            return {"status": "password must be at least 6 character"}, 404

        # Check email
        if args["email"] is not None:
            match=re.search("^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$", args["email"])
            if match is None:
                return {"status": "your input of email is wrong"}, 404

        # For status, status used to soft delete 
        if args["status"] == "True" or args["status"] == "true":
            args["status"] = True
        elif args["status"] == "False" or args["status"] == "false":
            args["status"] = False

        # For upload image in storage
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

            filename = "https://alta-online-learning.s3-ap-southeast-1.amazonaws.com/avatar/" + str(filename_key)
            filename = filename.replace(" ", "+")
        
        else:
            filename = None

        # For filled salt on field's table of mentee
        salt = uuid.uuid4().hex
        encoded = ("%s%s" % (args["password"], salt)).encode("utf-8")
        hash_pass = hashlib.sha512(encoded).hexdigest()

        result = Mentees(
            args["username"],
            hash_pass,
            args["full_name"],
            args["email"],
            args["address"],
            args["phone"],
            args["place_birth"],
            args["date_birth"],
            filename,
            args["background_education"],
            args["github"],
            args["description"],
            salt,
            args["status"]
        )

        db.session.add(result)
        db.session.commit()

        # For get token when register
        jwt_username = marshal(result, Mentees.jwt_claims_fields)
        jwt_username["status"] = "mentee"
        token = create_access_token(identity=args["username"], user_claims=jwt_username)

        # Add key token in response of endpoint
        result = marshal(result, Mentees.response_fields)
        result["token"] = token

        return result, 200

    # Endpoint for soft delete
    def put(self, id):
        # Check id in query or not
        qry_mentee = Mentees.query.get(id)
        if qry_mentee is None:
            return {'status': 'Mentee is NOT_FOUND'}, 404
        
        # Input update status 
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="form")
        args = parser.parse_args()
        
        # Change status for soft delete
        if args['status'] is not None:
            if args["status"] == "True" or args["status"] == "true":
                args["status"] = True
            elif args["status"] == "False" or args["status"] == "false":
                args["status"] = False
        else:
            return {"status": "NOT FILLED"}, 404
            
            qry_mentee.status = args['status']

        db.session.commit()

        return marshal(qry_mentee, Mentees.response_fields), 200

    # Endpoint for update field
    @mentee_required
    def patch(self, id):
        qry_mentee = Mentees.query.filter_by(status=True).filter_by(id=id).first()
        if qry_mentee is None:
            return {'status': 'Mentee is NOT_FOUND'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument("username", location="form")
        parser.add_argument("password", location="form")
        parser.add_argument("full_name", location="form")
        parser.add_argument("email", location="form")
        parser.add_argument("address", location="form")
        parser.add_argument("phone", location="form")
        parser.add_argument("place_birth", location="form")
        parser.add_argument("date_birth", location="form")
        parser.add_argument("avatar", type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument("background_education", location="form")
        parser.add_argument("github", location="form")
        parser.add_argument("description", location="form")
        args = parser.parse_args()

        if args['username'] is not None:
            # Check username
            if len(args["username"]) < 6:
                return {"status": "username must be at least 6 character"}, 404
            qry_mentee.username = args['username']

        if args['password'] is not None:
            # Check password
            if len(args["password"]) < 6:
                return {"status": "password must be 6 character"}, 404
            encoded = ("%s%s" % (args["password"], qry_mentee.salt)).encode("utf-8")
            hash_pass = hashlib.sha512(encoded).hexdigest()
            qry_mentee.password = hash_pass

        if args['full_name'] is not None:
            qry_mentee.full_name = args['full_name']

        if args['email'] is not None:
            # Check email
            match=re.search("^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$", args["email"])
            if match is None:
                return {"status": "your input of email is wrong"}, 404
            qry_mentee.email = args['email']

        if args['address'] is not None:
            qry_mentee.address = args['address']

        if args['phone'] is not None:
            # Check phone number
            phone = re.findall("^0[0-9]{7,14}", args["phone"])
            if phone == [] or phone[0] != str(args['phone']) or len(args["phone"]) > 15:
                return {"status": "phone number not match"}, 404
            qry_mentee.phone = args['phone']

        if args['place_birth'] is not None:
            qry_mentee.place_birth = args['place_birth']

        if args['date_birth'] is not None:
            qry_mentee.date_birth = args['date_birth']

        if args['avatar'] is not None:
            # Check avatar in query
            if qry_mentee.avatar is not None:
                filename = qry_mentee.avatar
                # Remove avatar in storage
                filename = "avatar/"+filename.split("/")[-1]
                filename = filename.replace("+", " ")

                # S3 Connect
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=app.config["ACCESS_KEY_ID"],
                    aws_secret_access_key=app.config["ACCESS_SECRET_KEY"]
                )

                s3.delete_object(Bucket=app.config["BUCKET_NAME"], Key=filename)
 
                # Change avatar in storage
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

                filename = "https://alta-online-learning.s3-ap-southeast-1.amazonaws.com/avatar/" + str(filename_key)
                filename = filename.replace(" ", "+")

                qry_mentee.avatar = filename

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

                filename = "https://alta-online-learning.s3-ap-southeast-1.amazonaws.com/avatar/" + str(filename_key)
                filename = filename.replace(" ", "+")

                qry_mentee.avatar = filename

        if args['background_education'] is not None:
            qry_mentee.background_education = args['background_education']

        if args['github'] is not None:
            qry_mentee.github = args['github']

        if args['description'] is not None:
            qry_mentee.description = args['description']

        db.session.commit()

        return marshal(qry_mentee, Mentees.response_fields), 200

    # Endpoint for delete mentee by id
    def delete(self, id):
        mentee = Mentees.query.get(id)
        
        if mentee is not None:
            filename = mentee.avatar
            if filename is not None:
                # Remove avatar in storage
                filename = "avatar/"+filename.split("/")[-1]
                filename = filename.replace("+", " ")

                # S3 Connect
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=app.config["ACCESS_KEY_ID"],
                    aws_secret_access_key=app.config["ACCESS_SECRET_KEY"]
                )

                s3.delete_object(Bucket=app.config["BUCKET_NAME"], Key=filename)
            
            # Remove database
            db.session.delete(mentee)
            db.session.commit()
            return {"status": "DELETED SUCCESS"}, 200
        
        return {"status": "ID NOT FOUND"}, 200


class MenteesAll(Resource):
    # For solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    # Endpoint to get all and sort by username, full_name and role
    @admin_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=("username", "full_name"))
        parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
        parser.add_argument('search', location='args', help='Key word is None')
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry_mentee = Mentees.query

        if args['search'] is not None:
            qry_mentee = qry_mentee.filter(
                Mentees.username.like('%'+args['search']+'%') |
                Mentees.full_name.like('%'+args['search']+'%') | 
                Mentees.address.like('%'+args['search']+'%') |
                Mentees.email.like('%'+args['search']+'%') |
                Mentees.phone.like('%'+args['search']+'%')
                )

        if args["orderby"] is not None:
            if args['orderby'] == "username":
                if args["sort"] == "desc":
                    qry_mentee = qry_mentee.order_by(desc(Mentees.username))
                else:
                    qry_mentee = qry_mentee.order_by(Mentees.username)
            elif args["orderby"] == "full_name":
                if args["sort"] == "desc":
                    qry_mentee = qry_mentee.order_by(desc(Mentees.full_name))
                else:
                    qry_mentee = qry_mentee.order_by(Mentees.full_name)

        rows = []
        for row in qry_mentee.limit(args['rp']).offset(offset).all():
            if row.status == True:
                row = marshal(row, Mentees.response_fields)
                rows.append(row)

        return rows, 200


class MenteesHistoryScore(Resource):
    # For solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    # Get profile mentee and history score
    @jwt_required
    def get(self, id):
        qry_mentee = Mentees.query.filter_by(status=True).filter_by(id=id).first()

        if qry_mentee is not None:
            mentee = marshal(qry_mentee, Mentees.response_fields)
            
            # Altatest
            altatest = HistoriesAltatest.query.filter_by(mentee_id=id).filter_by(status=True).first()

            mentee["altatest"] = altatest.score

            # History_phase
            qry_history_phase = HistoriesPhase.query.filter_by(mentee_id=id).filter_by(status=True).all()

            histories_phase = []
            for history_phase in qry_history_phase:
                history_phase = marshal(history_phase, HistoriesPhase.response_fields)
                phase = Phases.query.filter_by(status=True).filter_by(id=history_phase["phase_id"]).first()
                phase = marshal(phase, Phases.response_fields)
                history_phase["name_phase"] = phase
                phase = history_phase["phase_id"]
                
                # Check same phase id
                qry_history_module = HistoriesModule.query.filter_by(status=True).filter_by(mentee_id=id).all()
                histories_module = []
                for history_module in qry_history_module:
                    module = Modules.query.filter_by(status=True).filter_by(id=history_module.module_id).first()
                    if module.phase_id == phase:
                        histories_module.append(history_module)
                
                # Input module in the same phase
                modules = []
                for history_module in histories_module:
                    history_module = marshal(history_module, HistoriesModule.response_fields)
                    module = Modules.query.filter_by(status=True).filter_by(id=history_module["module_id"]).first()
                    module = marshal(module, Modules.response_fields)
                    history_module["name_module"] = module
                    module = history_module["module_id"]

                    # Check same module id
                    qry_history_subject = HistoriesSubject.query.filter_by(status=True).filter_by(mentee_id=id).all()
                    histories_subject = []
                    for history_subject in qry_history_subject:
                        subject = Subjects.query.filter_by(status=True).filter_by(id=history_subject.subject_id).first()
                        if subject.module_id == module:
                            histories_subject.append(history_subject)

                    # Input subject in the same module
                    subjects = []
                    for history_subject in histories_subject:
                        history_subject = marshal(history_subject, HistoriesSubject.response_fields)
                        subject = Subjects.query.filter_by(status=True).filter_by(id=history_subject["subject_id"]).first()
                        subject = marshal(subject, Subjects.response_fields)
                        history_subject["name_subject"] = subject
                        
                        # Get score exam
                        qry_exam = Exams.query.filter_by(subject_id=history_subject["subject_id"]).filter_by(status=True).first()
                        score_exam = []
                        if qry_exam is not None:
                            qry_history_exam = HistoriesExam.query.filter_by(mentee_id=id).filter_by(exam_id=qry_exam.id).filter_by(status=True).all()
                            
                            for history_exam in qry_history_exam:
                                score_exam.append(history_exam.score)

                        history_subject["score_exam"] = score_exam

                        subjects.append(history_subject)
                    
                    history_module["subject"] = subjects

                    modules.append(history_module)
                
                    history_phase["module"] = modules

                histories_phase.append(history_phase)

            mentee["phase"] = histories_phase
                            
            return mentee, 200
        
        return {"status": "Id Mentees not found"}, 404


class MenteesAllStatus(Resource):
    # For solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200
        
    # Endpoint to get all status of mentee 
    def get(self):
        qry_mentee = Mentees.query

        rows = []
        for row in qry_mentee:
            row = marshal(row, Mentees.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200

api.add_resource(MenteesAll, "")
api.add_resource(MenteesResource, "", "/<id>")
api.add_resource(MenteesHistoryScore, "", "/score/<id>")
api.add_resource(MenteesAllStatus, "", "/all")