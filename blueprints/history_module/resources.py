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
from blueprints import mentee_required

from .model import HistoriesModule
from ..admin.model import Admins
from ..mentee.model import Mentees
from ..phase.model import Phases
from ..module.model import Modules
from ..requirement_module.model import RequirementsModule
from ..subject.model import Subjects
from ..file_subject.model import FilesSubject
from ..exam.model import Exams
from ..quiz.model import Quizs
from ..question_quiz.model import QuestionsQuiz
from ..choice_quiz.model import ChoicesQuiz

bp_history_module = Blueprint("history_module", __name__)
api = Api(bp_history_module)


class HistoriesModuleResource(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for search history module by id
    def get(self, id=None):
        qry_history_module = HistoriesModule.query.filter_by(status=True).filter_by(id=id).first()

        if qry_history_module is not None:
            return marshal(qry_history_module, HistoriesModule.response_fields), 200
        
        return {"status": "Id history module not found"}, 404

    #endpoint for post history module
    @mentee_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("module_id", location="json", required=True)
        parser.add_argument("mentee_id", location="json", required=True)
        parser.add_argument("score", location="json", default=None)
        parser.add_argument("is_complete", location="json", type=bool, default=False)
        parser.add_argument("lock_key", location="json", type=bool, default=False)
        parser.add_argument("status", location="json", type=bool, default=True)
        args = parser.parse_args()

        #Check module and mentee is existance in database
        qry_history_module = HistoriesModule.query.filter_by(module_id=args["module_id"]).filter_by(mentee_id=args["mentee_id"]).filter_by(status=True).all()
        if len(qry_history_module) > 0:
            return {"status": "Module and Mentee is already there"}, 404

        #Check Id Mentee is in database or not
        qry_mentee = Mentees.query.get(args["mentee_id"])
        if qry_mentee is None:
            return {"status": "ID Mentee is Not Found"}, 404

        #Check Id Module is in database or not
        qry_module = Modules.query.get(args["module_id"])
        if qry_module is None:
            return {"status": "ID Module is Not Found"}, 404

        result = HistoriesModule(
            args["module_id"],
            args["mentee_id"],
            args["score"],
            args["is_complete"],
            args["lock_key"],
            args["status"]
        )

        db.session.add(result)
        db.session.commit()

        return marshal(result, HistoriesModule.response_fields), 200

    #endpoint for soft delete
    def put(self, id):
        #check id in query or not
        qry_history_module = HistoriesModule.query.get(id)
        if qry_history_module is None:
            return {'status': 'History Module is NOT_FOUND'}, 404

        #input update status 
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete
        if args['status'] is not None:
            qry_history_module.status = args['status']

        db.session.commit()

        return marshal(qry_history_module, HistoriesModule.response_fields), 200

    #endpoint for update field
    def patch(self, id):
        qry_history_module = HistoriesModule.query.filter_by(status=True).filter_by(id=id).first()
        if qry_history_module is None:
            return {'status': 'History Module is NOT_FOUND'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument("module_id", location="json")
        parser.add_argument("mentee_id", location="json")
        parser.add_argument("score", location="json")
        parser.add_argument("is_complete", location="json", type=bool)
        parser.add_argument("lock_key", location="json", type=bool)
        args = parser.parse_args()

        if args['module_id'] is not None:
            qry_history_module.module_id = args["module_id"]

        if args['mentee_id'] is not None:
            qry_history_module.mentee_id = args['mentee_id']
        
        if args['score'] is not None:
            qry_history_module.score = args['score']

        if args['is_complete'] is not None:
            qry_history_module.is_complete = args['is_complete']

        if args['lock_key'] is not None:
            qry_history_module.lock_key = args['lock_key']

        db.session.commit()

        return marshal(qry_history_module, HistoriesModule.response_fields), 200

    #endpoint for delete history module by id
    def delete(self, id):
        qry_history_module = HistoriesModule.query.get(id)
        
        if qry_history_module is not None:
            db.session.delete(qry_history_module)
            db.session.commit()

            return {"status": "DELETED SUCCESS"}, 200
        
        return {"status": "ID NOT FOUND"}, 404


class HistoriesModuleAll(Resource):
    #endpoint to get all and sort by score and created at
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=("score", "created_at"))
        parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry_history_module = HistoriesModule.query

        if args["orderby"] is not None:
            if args['orderby'] == "score":
                if args["sort"] == "desc":
                    qry_history_module = qry_history_module.order_by(desc(HistoriesModule.score))
                else:
                    qry_history_module = qry_history_module.order_by(HistoriesModule.score)
            if args['orderby'] == "created_at":
                if args["sort"] == "desc":
                    qry_history_module = qry_history_module.order_by(desc(HistoriesModule.created_at))
                else:
                    qry_history_module = qry_history_module.order_by(HistoriesModule.created_at)

        rows = []
        for row in qry_history_module.limit(args['rp']).offset(offset).all():
            if row.status == True:
                row = marshal(row, HistoriesModule.response_fields)
                rows.append(row)

        return rows, 200


class HistoriesModuleMentee(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint to show all module per masing-masing mentee
    @mentee_required
    def get(self):
        #get id mentee
        verify_jwt_in_request()
        claims = get_jwt_claims()
        mentee_id = claims["id"]

        #get history module mentee
        qry_history_module = HistoriesModule.query.filter_by(status=True).filter_by(mentee_id=mentee_id).all()
        
        histories_module = []
        for history_module in qry_history_module:
            history_module = marshal(history_module, HistoriesModule.response_fields)

            #get module in database
            qry_module = Modules.query.filter_by(status=True).filter_by(id=history_module["module_id"]).first()
            module = marshal(qry_module, Modules.response_fields)

            #get admin in database
            qry_admin = Admins.query.get(module["admin_id"])
            admin = marshal(qry_admin, Admins.response_fields)

            #input admin in object module
            module["admin"] = admin

            #input module in object history module
            history_module["module"] = module

            #get subject in database
            qry_subject = Subjects.query.filter_by(status=True).filter_by(module_id=module["id"]).all()
            subjects = []
            for subject in qry_subject:
                subject = marshal(subject, Subjects.response_fields)

                #get file_subject in database
                qry_file_subject = FilesSubject.query.filter_by(status=True).filter_by(subject_id=subject["id"]).order_by(FilesSubject.category_file).all()
                files_subject = []
                for file_subject in qry_file_subject:
                    file_subject = marshal(file_subject, FilesSubject.response_fields)

                    files_subject.append(file_subject)

                #input file_subject in object subject
                subject["file_subject"] = files_subject

                #exam
                qry_exam = Exams.query.filter_by(status=True).filter_by(subject_id=subject["id"]).first()
                exams = [marshal(qry_exam, Exams.response_fields)]
                
                #quiz
                qry_quiz = Quizs.query.filter_by(status=True).filter_by(exam_id=exams[0]["id"]).first()
                quizs = [marshal(qry_quiz, Quizs.response_fields)]

                #question
                qry_question = QuestionsQuiz.query.filter_by(status=True).filter_by(quiz_id=quizs[0]["id"]).all()
                questions = []
                for question in qry_question:
                    if question.status == True:
                        question = marshal(question, QuestionsQuiz.response_fields)
                        
                        qry_choice = ChoicesQuiz.query.filter_by(status=True).filter_by(question_id=question["id"])
                        choices = []
                        for choice in qry_choice:
                            if choice.status == True:
                                choice = marshal(choice, ChoicesQuiz.response_fields)
                                choices.append(choice)
                        
                        question["choice"] = choices
                        
                        questions.append(question)

                if len(qry_question) != 0:
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

            #input subject in object history module
            history_module["subject"] = subjects

            #requirement
            qry_requirement = RequirementsModule.query.filter_by(module_id=history_module["module_id"]).all()

            requirements = []
            for requirement in qry_requirement:
                if requirement.status == True:
                    requirement = marshal(requirement, RequirementsModule.response_fields)
                    requirements.append(requirement)

            history_module["requirement"] = requirements

            histories_module.append(history_module)

        return histories_module, 200

    #endpoint when register to post module per masing-masing mentee
    @mentee_required
    def post(self):
        #get id mentee
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        qry_history_module = HistoriesModule.query.filter_by(mentee_id=claims["id"]).first()

        if qry_history_module is None:
            phases = Phases.query.filter_by(status=True).all()
            history_modules = []

            for index_phase, phase in enumerate(phases):
                modules = Modules.query.filter_by(status=True).filter_by(phase_id=phase.id).all()

                for index_module, module in enumerate(modules):
                    score = None
                    is_complete = False
                    
                    if index_module == 0 and index_phase == 0:
                        lock_key = True
                    else:
                        lock_key = False
                    
                    status = True
                    
                    result = HistoriesModule(
                        module.id,
                        claims["id"],
                        score,
                        is_complete,
                        lock_key,
                        status
                    )

                    db.session.add(result)
                    db.session.commit()

                    result = marshal(result, HistoriesModule.response_fields)
                    history_modules.append(result)

            return history_modules, 200
        
        else:
            return {"status": "Mentee is already take the course"}, 404


class HistoriesModuleByIdPhase(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint to show module per masing-masing mentee by id phase
    @mentee_required
    def get(self, id=None):
        #get id mentee
        verify_jwt_in_request()
        claims = get_jwt_claims()
        mentee_id = claims["id"]

        #get history module mentee
        qry_history_module = HistoriesModule.query.filter_by(status=True).filter_by(mentee_id=mentee_id).all()
        
        phase_id = int(id)

        histories_module = []
        for history_module in qry_history_module:
            history_module = marshal(history_module, HistoriesModule.response_fields)

            #get module in database
            qry_module = Modules.query.filter_by(status=True).filter_by(id=history_module["module_id"]).first()
            module = marshal(qry_module, Modules.response_fields)

            if module["phase_id"] == phase_id:
                #get admin in database
                qry_admin = Admins.query.get(module["admin_id"])
                admin = marshal(qry_admin, Admins.response_fields)

                #input admin in object module
                module["admin"] = admin

                #input module in object history module
                history_module["module"] = module

                #get subject in database
                qry_subject = Subjects.query.filter_by(status=True).filter_by(module_id=module["id"]).all()
                subjects = []
                for subject in qry_subject:
                    subject = marshal(subject, Subjects.response_fields)

                    #get file_subject in database
                    qry_file_subject = FilesSubject.query.filter_by(status=True).filter_by(subject_id=subject["id"]).order_by(FilesSubject.category_file).all()
                    files_subject = []
                    for file_subject in qry_file_subject:
                        file_subject = marshal(file_subject, FilesSubject.response_fields)

                        files_subject.append(file_subject)

                    #input file_subject in object subject
                    subject["file_subject"] = files_subject

                    #exam
                    qry_exam = Exams.query.filter_by(status=True).filter_by(subject_id=subject["id"]).first()
                    exams = [marshal(qry_exam, Exams.response_fields)]
                    
                    #quiz
                    qry_quiz = Quizs.query.filter_by(status=True).filter_by(exam_id=exams[0]["id"]).first()
                    quizs = [marshal(qry_quiz, Quizs.response_fields)]

                    #question
                    qry_question = QuestionsQuiz.query.filter_by(status=True).filter_by(quiz_id=quizs[0]["id"]).all()
                    questions = []
                    for question in qry_question:
                        if question.status == True:
                            question = marshal(question, QuestionsQuiz.response_fields)
                            
                            qry_choice = ChoicesQuiz.query.filter_by(status=True).filter_by(question_id=question["id"])
                            choices = []
                            for choice in qry_choice:
                                if choice.status == True:
                                    choice = marshal(choice, ChoicesQuiz.response_fields)
                                    choices.append(choice)
                            
                            question["choice"] = choices
                            
                            questions.append(question)

                    if len(qry_question) != 0:
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

                #input subject in object history module
                history_module["subject"] = subjects

                #requirement
                qry_requirement = RequirementsModule.query.filter_by(module_id=history_module["module_id"]).all()

                requirements = []
                for requirement in qry_requirement:
                    if requirement.status == True:
                        requirement = marshal(requirement, RequirementsModule.response_fields)
                        requirements.append(requirement)

                history_module["requirement"] = requirements

                histories_module.append(history_module)

        return histories_module, 200


class HistoriesModuleAllStatus(Resource):
    #endpoint to get all status of history subject
    def get(self):
        qry_history_module = HistoriesModule.query

        rows = []
        for row in qry_history_module:
            row = marshal(row, HistoriesModule.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200

api.add_resource(HistoriesModuleAll, "")
api.add_resource(HistoriesModuleResource, "", "/<id>")
api.add_resource(HistoriesModuleAllStatus, "", "/all")
api.add_resource(HistoriesModuleMentee, "", "/mentee")
api.add_resource(HistoriesModuleByIdPhase, "", "/subject/<id>")