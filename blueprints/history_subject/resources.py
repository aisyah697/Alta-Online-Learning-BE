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

from .model import HistoriesSubject
from ..mentee.model import Mentees
from ..phase.model import Phases
from ..module.model import Modules
from ..subject.model import Subjects
from ..file_subject.model import FilesSubject
from ..exam.model import Exams
from ..quiz.model import Quizs
from ..question_quiz.model import QuestionsQuiz
from ..choice_quiz.model import ChoicesQuiz

bp_history_subject = Blueprint("history_subject", __name__)
api = Api(bp_history_subject)


class HistoriesSubjectResource(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for search history subject by id
    @mentee_required
    def get(self, id=None):
        #check mentee id
        verify_jwt_in_request()
        claims = get_jwt_claims()
        mentee_id = claims["id"]

        qry_history_subject = HistoriesSubject.query.filter_by(status=True).filter_by(id=id).first()

        if qry_history_subject is None:
            return {"status": "Id history subject not found"}, 404

        if qry_history_subject.mentee_id != mentee_id:
            return {"status": "mentee_id in token and history subject isn't match"}, 404

        if qry_history_subject is not None:
            qry_exam = Exams.query.filter_by(subject_id=qry_history_subject.subject_id).first()
            exam = marshal(qry_exam, Exams.response_fields)

            history_subject = marshal(qry_history_subject, HistoriesSubject.response_fields)

            history_subject["exam"] = exam

            return history_subject, 200

    #endpoint for post history subject
    @mentee_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("subject_id", location="json", required=True)
        parser.add_argument("mentee_id", location="json", required=True)
        parser.add_argument("score", location="json", default=None)
        parser.add_argument("time_of_exam", location="json", default=None)
        parser.add_argument("is_complete", location="json", type=bool, default=False)
        parser.add_argument("lock_key", location="json", type=bool, default=False)
        parser.add_argument("status", location="json", type=bool, default=True)
        args = parser.parse_args()

        #Check subject and mentee is existance in database
        qry_history_subject = HistoriesSubject.query.filter_by(subject_id=args["subject_id"]).filter_by(mentee_id=args["mentee_id"]).filter_by(status=True).all()
        if len(qry_history_subject) > 0:
            return {"status": "Subject and Mentee is already there"}, 404

        #Check Id Mentee is in database or not
        qry_mentee = Mentees.query.get(args["mentee_id"])
        if qry_mentee is None:
            return {"status": "ID Mentee is Not Found"}, 404

        #Check Id Subject is in database or not
        qry_subject = Subjects.query.get(args["subject_id"])
        if qry_subject is None:
            return {"status": "ID Subject is Not Found"}, 404

        if args["score"] is not None:
            if int(args["score"]) >= 80:
                args["is_complete"] = True
            else:
                args["is_complete"] = False

        result = HistoriesSubject(
            args["subject_id"],
            args["mentee_id"],
            args["score"],
            args["time_of_exam"],
            args["is_complete"],
            args["lock_key"],
            args["status"]
        )

        db.session.add(result)
        db.session.commit()

        return marshal(result, HistoriesSubject.response_fields), 200

    #endpoint for soft delete
    def put(self, id):
        #check id in querry or not
        qry_history_subject = HistoriesSubject.query.get(id)
        if qry_history_subject is None:
            return {'status': 'History Subject is NOT_FOUND'}, 404

        #input update status 
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete
        if args['status'] is not None:
            qry_history_subject.status = args['status']

        db.session.commit()

        return marshal(qry_history_subject, HistoriesSubject.response_fields), 200

    #endpoint for update field
    def patch(self, id):
        qry_history_subject = HistoriesSubject.query.filter_by(status=True).filter_by(id=id).first()
        if qry_history_subject is None:
            return {'status': 'History Subject is NOT_FOUND'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument("subject_id", location="json")
        parser.add_argument("mentee_id", location="json")
        parser.add_argument("score", location="json", default=None)
        parser.add_argument("time_of_exam", location="json", default=None)
        parser.add_argument("is_complete", location="json", type=bool, default=False)
        parser.add_argument("lock_key", location="json", type=bool, default=False)
        args = parser.parse_args()

        if args['subject_id'] is not None:
            qry_history_subject.subject_id = args["subject_id"]

        if args['mentee_id'] is not None:
            qry_history_subject.mentee_id = args['mentee_id']
        
        if args['time_of_exam'] is not None:
            qry_history_subject.time_of_exam = args['time_of_exam']

        if args['score'] is not None:
            qry_history_subject.score = args['score']
            if int(args["score"]) >= 80:
                args["is_complete"] = True
            else:
                args["is_complete"] = False

            qry_history_subject.is_complete = args['is_complete']

        db.session.commit()

        return marshal(qry_history_subject, HistoriesSubject.response_fields), 200

    #endpoint for delete history subject by id
    def delete(self, id):
        qry_history_subject = HistoriesSubject.query.get(id)
        
        if qry_history_subject is not None:
            db.session.delete(qry_history_subject)
            db.session.commit()

            return {"status": "DELETED SUCCESS"}, 200
        
        return {"status": "ID NOT FOUND"}, 404


class HistoriesSubjectAll(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200
    
    #endpoint to get all and sort by score and created at
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=("score", "created_at"))
        parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry_history_subject = HistoriesSubject.query

        if args["orderby"] is not None:
            if args['orderby'] == "score":
                if args["sort"] == "desc":
                    qry_history_subject = qry_history_subject.order_by(desc(HistoriesSubject.score))
                else:
                    qry_history_subject = qry_history_subject.order_by(HistoriesSubject.score)
            if args['orderby'] == "created_at":
                if args["sort"] == "desc":
                    qry_history_subject = qry_history_subject.order_by(desc(HistoriesSubject.created_at))
                else:
                    qry_history_subject = qry_history_subject.order_by(HistoriesSubject.created_at)

        rows = []
        for row in qry_history_subject.limit(args['rp']).offset(offset).all():
            if row.status == True:
                row = marshal(row, HistoriesSubject.response_fields)
                rows.append(row)

        return rows, 200


class HistoriesSubjectMentee(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint to show all subject per masing-masing mentee
    @mentee_required
    def get(self):
        #get id mentee
        verify_jwt_in_request()
        claims = get_jwt_claims()
        mentee_id = claims["id"]

        #get history subject mentee
        qry_history_subject = HistoriesSubject.query.filter_by(status=True).filter_by(mentee_id=mentee_id).all()

        histories_subject = []
        for history_subject in qry_history_subject:
            history_subject = marshal(history_subject, HistoriesSubject.response_fields)
            
            #get subject in database
            qry_subject = Subjects.query.filter_by(status=True).filter_by(id=history_subject["subject_id"]).first()
            subject = marshal(qry_subject, Subjects.response_fields)
            
            #input subject in object history subject
            history_subject["subject"] = subject

            #get file_subject in database
            qry_file_subject = FilesSubject.query.filter_by(status=True).filter_by(subject_id=subject["id"]).order_by(FilesSubject.category_file).all()
            files_subject = []
            for file_subject in qry_file_subject:
                file_subject = marshal(file_subject, FilesSubject.response_fields)

                files_subject.append(file_subject)

            #input file_subject in object history subject
            history_subject["file_subject"] = files_subject

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

            if qry_question is not None:
                quizs[0]["question"] = questions
            else:
                quizs[0]["question"] = []

            if qry_quiz is not None:
                exams[0]["quiz"] = quizs
            else:
                exams[0]["quiz"] = []

            if qry_exam is not None:
                history_subject["exam"] = exams
            else:
                history_subject["exam"] = []

            histories_subject.append(history_subject)

        return histories_subject, 200

    #endpoint when register to post phase per masing-masing mentee
    @mentee_required
    def post(self):
        #get id mentee
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        qry_history_subject = HistoriesSubject.query.filter_by(mentee_id=claims["id"]).first()

        if qry_history_subject is None:
            subjects = Subjects.query.filter_by(status=True).all()

            history_subjects = []
            for index, subject in enumerate(subjects):
                score = None
                time_of_exam = None
                is_complete = False
                
                if index == 0:
                    lock_key = True
                else:
                    lock_key = False
                
                status = True
                
                result = HistoriesSubject(
                    subject.id,
                    claims["id"],
                    score,
                    time_of_exam,
                    is_complete,
                    lock_key,
                    status
                )

                db.session.add(result)
                db.session.commit()

                result = marshal(result, HistoriesSubject.response_fields)
                history_subjects.append(result)
            
            return history_subjects, 200
        
        else:
            return {"status": "Mentee is already take the course"}, 404


class HistoriesSubjectByIdModule(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint to show subject per masing-masing mentee by id module
    @mentee_required
    def get(self, id=None):
        #get id mentee
        verify_jwt_in_request()
        claims = get_jwt_claims()
        mentee_id = claims["id"]

        #get history subject mentee
        qry_history_subject = HistoriesSubject.query.filter_by(status=True).filter_by(mentee_id=mentee_id).all()

        module_id = int(id)

        histories_subject = []
        for history_subject in qry_history_subject:
            history_subject = marshal(history_subject, HistoriesSubject.response_fields)
            
            #get subject in database
            qry_subject = Subjects.query.filter_by(status=True).filter_by(id=history_subject["subject_id"]).first()
            subject = marshal(qry_subject, Subjects.response_fields)
            
            if subject["module_id"] == module_id:
                #input subject in object history subject
                history_subject["subject"] = subject

                #get file_subject in database
                qry_file_subject = FilesSubject.query.filter_by(status=True).filter_by(subject_id=subject["id"]).order_by(FilesSubject.category_file).all()
                files_subject = []
                for file_subject in qry_file_subject:
                    file_subject = marshal(file_subject, FilesSubject.response_fields)

                    files_subject.append(file_subject)

                #input file_subject in object history subject
                history_subject["file_subject"] = files_subject

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

                if qry_question is not None:
                    quizs[0]["question"] = questions
                else:
                    quizs[0]["question"] = []

                if qry_quiz is not None:
                    exams[0]["quiz"] = quizs
                else:
                    exams[0]["quiz"] = []

                if qry_quiz is not None:
                    history_subject["exam"] = exams
                else:
                    history_subject["exam"] = []

                histories_subject.append(history_subject)

        return histories_subject, 200


class HistoriesSubjectAllStatus(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200
    
    #endpoint to get all status of history subject
    def get(self):
        qry_history_subject = HistoriesSubject.query

        rows = []
        for row in qry_history_subject:
            row = marshal(row, HistoriesSubject.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200

api.add_resource(HistoriesSubjectAll, "")
api.add_resource(HistoriesSubjectResource, "", "/<id>")
api.add_resource(HistoriesSubjectAllStatus, "", "/all")
api.add_resource(HistoriesSubjectMentee, "", "/mentee")
api.add_resource(HistoriesSubjectByIdModule, "", "/subject/<id>")