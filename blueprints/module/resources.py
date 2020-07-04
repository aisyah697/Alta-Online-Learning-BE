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

from .model import Modules
from ..phase.model import Phases
from ..admin.model import Admins
from ..subject.model import Subjects
from ..requirement_module.model import RequirementsModule
from ..file_subject.model import FilesSubject
from ..exam.model import Exams
from ..quiz.model import Quizs
from ..question_quiz.model import QuestionsQuiz
from ..choice_quiz.model import ChoicesQuiz

bp_module = Blueprint("module", __name__)
api = Api(bp_module)


class ModulesResource(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for search module by id
    @admin_required
    def get(self, id=None):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            qry_module = Modules.query.filter_by(status=True).filter_by(id=id).first()

            if qry_module is not None:
                return marshal(qry_module, Modules.response_fields), 200
            
            return {"status": "Id Modules not found"}, 404

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    #endpoint for post module
    @admin_required
    def post(self):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super":
            parser = reqparse.RequestParser()
            parser.add_argument("admin_id", location="form", required=True)
            parser.add_argument("phase_id", location="form", required=True)
            parser.add_argument("name", location="form")
            parser.add_argument("description", location="form")
            parser.add_argument("image", type=werkzeug.datastructures.FileStorage, location='files')
            parser.add_argument("status", location="form", default="True")
            args = parser.parse_args()

            #check phase_id
            phase_id = Phases.query.get(args["phase_id"])

            if phase_id is None:
                return {"status": "Phase isn't in database"}, 404

            #check admin_id
            admin_id = Admins.query.get(args["admin_id"])

            if admin_id is None:
                return {"status": "Admin isn't in database"}, 404

            #for status, status used to soft delete 
            if args["status"] == "True" or args["status"] == "true":
                args["status"] = True
            elif args["status"] == "False" or args["status"] == "false":
                args["status"] = False
            
            #for upload image in storage
            module_image = args["image"]

            if module_image:
                randomstr = uuid.uuid4().hex
                filename_key = randomstr + "_" + module_image.filename
                filename_body = module_image

                # S3 Connect
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=app.config["ACCESS_KEY_ID"],
                    aws_secret_access_key=app.config["ACCESS_SECRET_KEY"]
                )

                # Image Uploaded
                s3.put_object(Bucket=app.config["BUCKET_NAME"], Key="image/"+filename_key, Body=filename_body, ACL='public-read')

                filename = "https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/image/" + str(filename_key)
                filename = filename.replace(" ", "+")
            
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

        else:
            return {"status": "admin isn't at role super admin"}, 404

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
    @admin_required
    def patch(self, id):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super":
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
                    #remove image in storage
                    filename = "image/"+filename.split("/")[-1]
                    filename = filename.replace("+", " ")

                    # S3 Connect
                    s3 = boto3.client(
                        's3',
                        aws_access_key_id=app.config["ACCESS_KEY_ID"],
                        aws_secret_access_key=app.config["ACCESS_SECRET_KEY"]
                    )

                    s3.delete_object(Bucket=app.config["BUCKET_NAME"], Key=filename)
    
                    # #change image in storage
                    image = args["image"]

                    randomstr = uuid.uuid4().hex
                    filename_key = randomstr + "_" + image.filename
                    filename_body = image

                    # S3 Connect
                    s3 = boto3.client(
                        's3',
                        aws_access_key_id=app.config["ACCESS_KEY_ID"],
                        aws_secret_access_key=app.config["ACCESS_SECRET_KEY"]
                    )

                    # Image Uploaded
                    s3.put_object(Bucket=app.config["BUCKET_NAME"], Key="image/"+filename_key, Body=filename_body, ACL='public-read')

                    filename = "https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/image/" + str(filename_key)
                    filename = filename.replace(" ", "+")

                    qry_module.image = filename

                else:
                    image = args["image"]

                    randomstr = uuid.uuid4().hex
                    filename_key = randomstr + "_" + image.filename
                    filename_body = image

                    # S3 Connect
                    s3 = boto3.client(
                        's3',
                        aws_access_key_id=app.config["ACCESS_KEY_ID"],
                        aws_secret_access_key=app.config["ACCESS_SECRET_KEY"]
                    )

                    # Image Uploaded
                    s3.put_object(Bucket=app.config["BUCKET_NAME"], Key="image/"+filename_key, Body=filename_body, ACL='public-read')

                    filename = "https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/image/" + str(filename_key)
                    filename = filename.replace(" ", "+")

                    qry_module.image = filename

            db.session.commit()

            return marshal(qry_module, Modules.response_fields), 200

        else:
            return {"status": "admin isn't at role super admin"}, 404

    #endpoint for delete module by id
    @admin_required
    def delete(self, id):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super":
            module = Modules.query.get(id)
            filename = module.image
            
            if module is not None:
                if filename is not None:
                    #remove image in storage
                    filename = "image/"+filename.split("/")[-1]
                    filename = filename.replace("+", " ")

                    # S3 Connect
                    s3 = boto3.client(
                        's3',
                        aws_access_key_id=app.config["ACCESS_KEY_ID"],
                        aws_secret_access_key=app.config["ACCESS_SECRET_KEY"]
                    )

                    s3.delete_object(Bucket=app.config["BUCKET_NAME"], Key=filename)
                
                #remove database
                db.session.delete(module)
                db.session.commit()
                return {"status": "DELETED SUCCESS"}, 200
            
            return {"status": "ID NOT FOUND"}, 200

        else:
            return {"status": "admin isn't at role super admin"}, 404


class ModulesAll(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint to get all and sort by admin_id, phase_id and name
    @admin_required
    def get(self):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
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

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class ModuleNestedById(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    @admin_required
    def get(self, id=None):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            #Module
            qry_module = Modules.query.get(id)
            
            if qry_module is not None and qry_module.status == True:
                module = marshal(qry_module, Modules.response_fields)

                if claims["id"] == module["admin_id"] or claims["role"] == "super":
                    #admin
                    qry_admin = Admins.query.filter_by(id=module["admin_id"]).first()
                    admin = marshal(qry_admin, Admins.response_fields)
                    module["admin"] = admin

                    #Subject
                    qry_subject = Subjects.query.filter_by(module_id=module["id"]).all()
                    
                    subjects = []
                    for subject in qry_subject:
                        if subject.status == True:
                            subject = marshal(subject, Subjects.response_fields)
                            #File Subject
                            qry_file_subject = FilesSubject.query.filter_by(subject_id=subject["id"]).all()
                            
                            videos = []
                            presentations = []
                            for file_subject in qry_file_subject:
                                if file_subject.status == True:
                                    if file_subject.category_file == "video":
                                        file_subject = marshal(file_subject, FilesSubject.response_fields)
                                        videos.append(file_subject)
                                    elif file_subject.category_file == "presentation":
                                        file_subject = marshal(file_subject, FilesSubject.response_fields)
                                        presentations.append(file_subject)

                            subject["video"] = videos
                            subject["presentation"] = presentations

                            #exam
                            qry_exam = Exams.query.filter_by(status=True).filter_by(subject_id=subject["id"]).first()
                            exams = [marshal(qry_exam, Exams.response_fields)]
                            
                            #quiz
                            qry_quiz = Quizs.query.filter_by(status=True).filter_by(exam_id=exams[0]["id"]).first()
                            quizs = [marshal(qry_quiz, Quizs.response_fields)]

                            #question
                            qry_question = QuestionsQuiz.query.filter_by(quiz_id=quizs[0]["id"]).all()
                            questions = []
                            for question in qry_question:
                                if question.status == True:
                                    question = marshal(question, QuestionsQuiz.response_fields)
                                    
                                    qry_choice = ChoicesQuiz.query.filter_by(question_id=question["id"])
                                    choices = []
                                    for choice in qry_choice:
                                        if choice.status == True:
                                            choice = marshal(choice, ChoicesQuiz.response_fields)
                                            choices.append(choice)
                                    
                                    question["choice"] = choices
                                    
                                    questions.append(question)

                            if qry_question is not None:
                                quizs[0]["question"] = questions
                            else:
                                quizs[0]["question"] = []

                            if qry_quiz is not None:
                                exams[0]["quiz"] = quizs
                            else:
                                exams[0]["quiz"] = []

                            if qry_exam is not None:
                                subject["exam"] = exams
                            else:
                                subject["exam"] = []

                            subjects.append(subject)
                    
                    #requirement
                    qry_requirement = RequirementsModule.query.filter_by(module_id=module["id"]).all()

                    requirements = []
                    for requirement in qry_requirement:
                        if requirement.status == True:
                            requirement = marshal(requirement, RequirementsModule.response_fields)
                            requirements.append(requirement)

                    module["subject"] = subjects
                    module["requirement"] = requirements
                
                else:
                    return {"status": "admin isn't permission to access this module"}, 404
                
                return module, 200

            else:
                return {"status": "module is not found"}, 404

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class ModuleNestedAll(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    @admin_required
    def get(self, id=None):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=25)
            parser.add_argument('orderby', location='args', help='invalid status', choices=("id", "created_at"))
            parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']

            qry_module = Modules.query

            if args["orderby"] is not None:
                if args['orderby'] == "id":
                    if args["sort"] == "desc":
                        qry_module = qry_module.order_by(desc(Modules.id))
                    else:
                        qry_module = qry_module.order_by(Modules.id)
                elif args["orderby"] == "created_at":
                    if args["sort"] == "desc":
                        qry_module = qry_module.order_by(desc(Modules.created_at))
                    else:
                        qry_module = qry_module.order_by(Modules.created_at)

            modules = []
            for module in qry_module.limit(args['rp']).offset(offset).all():
                if module.status == True and (module.admin_id == claims["id"] or claims["role"] == "super"):
                    module = marshal(module, Modules.response_fields)

                    #admin
                    qry_admin = Admins.query.filter_by(id=module["admin_id"]).first()
                    admin = marshal(qry_admin, Admins.response_fields)
                    module["admin"] = admin

                    qry_subject = Subjects.query.filter_by(module_id=module["id"]).all()    
                    subjects = []
                    for subject in qry_subject:
                        if subject.status == True:
                            subject = marshal(subject, Subjects.response_fields)
                            #File Subject
                            qry_file_subject = FilesSubject.query.filter_by(subject_id=subject["id"]).all()
                            
                            videos = []
                            presentations = []
                            for file_subject in qry_file_subject:
                                if file_subject.status == True:
                                    if file_subject.category_file == "video":
                                        file_subject = marshal(file_subject, FilesSubject.response_fields)
                                        videos.append(file_subject)
                                    elif file_subject.category_file == "presentation":
                                        file_subject = marshal(file_subject, FilesSubject.response_fields)
                                        presentations.append(file_subject)

                            subject["video"] = videos
                            subject["presentation"] = presentations

                            #exam
                            qry_exam = Exams.query.filter_by(status=True).filter_by(subject_id=subject["id"]).first()
                            exams = [marshal(qry_exam, Exams.response_fields)]
                            
                            #quiz
                            qry_quiz = Quizs.query.filter_by(status=True).filter_by(exam_id=exams[0]["id"]).first()
                            quizs = [marshal(qry_quiz, Quizs.response_fields)]

                            #question
                            qry_question = QuestionsQuiz.query.filter_by(quiz_id=quizs[0]["id"]).all()
                            questions = []
                            for question in qry_question:
                                if question.status == True:
                                    question = marshal(question, QuestionsQuiz.response_fields)
                                    
                                    qry_choice = ChoicesQuiz.query.filter_by(question_id=question["id"])
                                    choices = []
                                    for choice in qry_choice:
                                        if choice.status == True:
                                            choice = marshal(choice, ChoicesQuiz.response_fields)
                                            choices.append(choice)
                                    
                                    question["choice"] = choices
                                    
                                    questions.append(question)

                            if qry_question is not None:
                                quizs[0]["question"] = questions
                            else:
                                quizs[0]["question"] = []

                            if qry_quiz is not None:
                                exams[0]["quiz"] = quizs
                            else:
                                exams[0]["quiz"] = []

                            if qry_exam is not None:
                                subject["exam"] = exams
                            else:
                                subject["exam"] = []

                            subjects.append(subject)
                    
                    #requirement
                    qry_requirement = RequirementsModule.query.filter_by(module_id=module["id"]).all()

                    requirements = []
                    for requirement in qry_requirement:
                        if requirement.status == True:
                            requirement = marshal(requirement, RequirementsModule.response_fields)
                            requirements.append(requirement)

                    module["subject"] = subjects
                    module["requirement"] = requirements

                    modules.append(module)

            return modules, 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class ModulesAllStatus(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200
    
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
api.add_resource(ModuleNestedById, "", "/nested/<id>")
api.add_resource(ModuleNestedAll, "", "/nested")
api.add_resource(ModulesAllStatus, "", "/all")