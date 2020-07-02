import json
import os
import werkzeug
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

from .model import Subjects
from ..module.model import Modules
from ..admin.model import Admins
from ..subject.model import Subjects
from ..requirement_module.model import RequirementsModule
from ..file_subject.model import FilesSubject
from ..exam.model import Exams
from ..quiz.model import Quizs
from ..question_quiz.model import QuestionsQuiz
from ..choice_quiz.model import ChoicesQuiz

bp_subject = Blueprint("subject", __name__)
api = Api(bp_subject)


class SubjectsResource(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for search subject by id
    @admin_required
    def get(self, id=None):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            qry_subject = Subjects.query.filter_by(status=True).filter_by(id=id).first()

            if qry_subject is not None:
                return marshal(qry_subject, Subjects.response_fields), 200
            
            return {"status": "Id Subject not found"}, 404

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    #endpoint for post subject
    @admin_required
    def post(self):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            parser = reqparse.RequestParser()
            parser.add_argument("module_id", location="json", required=True)
            parser.add_argument("name", location="json")
            parser.add_argument("description", location="json")
            parser.add_argument("quesioner", location="json")
            parser.add_argument("status", location="json", default=True, type=bool)
            args = parser.parse_args()

            #check module_id
            module_id = Modules.query.get(args["module_id"])

            if module_id is None:
                return {"status": "Module isn't in database"}, 404

            result = Subjects(
                args["module_id"],
                args["name"],
                args["description"],
                args["quesioner"],
                args["status"]
            )

            db.session.add(result)
            db.session.commit()

            return marshal(result, Subjects.response_fields), 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    #endpoint for soft delete
    def put(self, id):
        #check id in query or not
        qry_subject = Subjects.query.get(id)
        if qry_subject is None:
            return {'status': 'Mentee is NOT_FOUND'}, 404

        #input update status 
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete
        qry_subject.status = args["status"]

        db.session.commit()

        return marshal(qry_subject, Subjects.response_fields), 200

    #endpoint for update field
    @admin_required
    def patch(self, id):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            #check id in querry or not
            qry_subject = Subjects.query.filter_by(status=True).filter_by(id=id).first()
            if qry_subject is None:
                return {'status': 'Mentee is NOT_FOUND'}, 404

            parser = reqparse.RequestParser()
            parser.add_argument("name", location="json")
            parser.add_argument("description", location="json")
            parser.add_argument("quesioner", location="json")
            args = parser.parse_args()

            if args['name'] is not None:
                qry_subject.name = args["name"]
            
            if args['description'] is not None:
                qry_subject.description = args["description"]
            
            if args['quesioner'] is not None:
                qry_subject.quesioner = args["quesioner"]

            db.session.commit()

            return marshal(qry_subject, Subjects.response_fields), 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    #endpoint for delete subject by id
    @admin_required
    def delete(self, id):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            qry_subject = Subjects.query.get(id)
            
            if qry_subject is not None:
                db.session.delete(qry_subject)
                db.session.commit()
                
                return {"status": "DELETED SUCCESS"}, 200
            
            return {"status": "ID NOT FOUND"}, 404

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class SubjectsAll(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint to get all and sort by name & modul_id
    @admin_required
    def get(self):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=25)
            parser.add_argument('orderby', location='args', help='invalid status', choices=("name", "module_id"))
            parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']

            qry_subject = Subjects.query

            if args["orderby"] is not None:
                if args['orderby'] == "name":
                    if args["sort"] == "desc":
                        qry_subject = qry_subject.order_by(desc(Subjects.name))
                    else:
                        qry_subject = qry_subject.order_by(Subjects.name)
                elif args['orderby'] == "module_id":
                    if args["sort"] == "desc":
                        qry_subject = qry_subject.order_by(desc(Subjects.module_id))
                    else:
                        qry_subject = qry_subject.order_by(Subjects.module_id)

            rows = []
            for row in qry_subject.limit(args['rp']).offset(offset).all():
                if row.status == True:
                    row = marshal(row, Subjects.response_fields)
                    rows.append(row)

            if rows == []:
                return {"status": "data not found"}, 404

            return rows, 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class SubjectNestedById(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    @admin_required
    def get(self, id=None):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            #Subject
            qry_subject = Subjects.query.get(id)
            
            if qry_subject is not None and qry_subject.status == True:
                subject = marshal(qry_subject, Subjects.response_fields)

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

                quizs[0]["question"] = questions

                exams[0]["quiz"] = quizs

                subject["exam"] = exams
                
                return subject, 200

            else:
                return {"status": "subject is not found"}, 404

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class SubjectNestedAll(Resource):
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

            qry_subject = Subjects.query

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

            subjects = []
            for subject in qry_subject.limit(args['rp']).offset(offset).all():
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

                    quizs[0]["question"] = questions

                    exams[0]["quiz"] = quizs

                    subject["exam"] = exams

                    subjects.append(subject)

            return subjects, 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class SubjectsAllStatus(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint to get all status of subject
    def get(self):
        qry_subject = Subjects.query

        rows = []
        for row in qry_subject:
            row = marshal(row, Subjects.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200

api.add_resource(SubjectsAll, "")
api.add_resource(SubjectsResource, "", "/<id>")
api.add_resource(SubjectNestedById, "", "/nested/<id>")
api.add_resource(SubjectNestedAll, "", "/nested")
api.add_resource(SubjectsAllStatus, "", "/all")