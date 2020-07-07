import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app
from sqlalchemy import desc
from flask_jwt_extended import (
    JWTManager,
    get_jwt_identity,
    verify_jwt_in_request,
    jwt_required,
    get_jwt_claims,
)
from blueprints import mentee_required

from .model import CorrectionsExam
from ..history_phase.model import HistoriesPhase
from ..history_module.model import HistoriesModule
from ..history_subject.model import HistoriesSubject
from ..history_exam.model import HistoriesExam
from ..module.model import Modules
from ..subject.model import Subjects
from ..question_quiz.model import QuestionsQuiz
from ..choice_quiz.model import ChoicesQuiz
from ..exam.model import Exams
from ..quiz.model import Quizs

bp_correction_exam = Blueprint("correction_exam", __name__)
api = Api(bp_correction_exam)

class CorrectionsExamResource(Resource):
    # endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for show correction quiz
    @mentee_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("question_quiz_id", location="json", required=True)
        args = parser.parse_args()
        
        #get mentee_id from id authentification
        verify_jwt_in_request()
        claims = get_jwt_claims()

        #get history_altatest_id from mentee_id
        qry_history_exam = HistoriesExam.query.filter_by(mentee_id=claims["id"]).first()

        qry_correction_exam = CorrectionsExam.query.filter_by(status=True).filter_by(question_quiz_id=args["question_quiz_id"]).filter_by(history_exam_id=qry_history_exam.id).all()

        if qry_correction_exam == []:
            return {"status": "Answer of this question is not found"}, 404

        return marshal(qry_correction_exam, CorrectionsExam.response_fields), 200

    @mentee_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("history_exam_id", location="json", required=True)
        parser.add_argument("question_quiz_id", location="json", required=True)
        parser.add_argument("answer_quiz_id", location="json", default=None)
        args = parser.parse_args()

        #check input history_exam_id in database there or not
        qry_history_exam = HistoriesExam.query.filter_by(id=args["history_exam_id"]).filter_by(status=True).first()
        if qry_history_exam is None:
            return {"status": "Input history exam isn't in database"}, 403

        #check mentee from token match with mentee from history_exam
        verify_jwt_in_request
        claims = get_jwt_claims()

        if claims["id"] != qry_history_exam.mentee_id:
            return {"status": "mentee in token and history_exam isn't match"}, 403
        
        #check input question is in database or not
        qry_question_exam = QuestionsQuiz.query.filter_by(id=args["question_quiz_id"]).filter_by(status=True).first()
        if qry_history_exam is None:
            return {"status": "input question isn't in database"}, 403

        #check input answer isn't at database and match with question
        if args["answer_quiz_id"] is not None:
            #check input answer isn't at database
            qry_choice_exam = ChoicesQuiz.query.filter_by(id=args["answer_quiz_id"]).filter_by(status=True).first()
            if qry_choice_exam is None:
                return {"status": "input answer isn't in database"}, 403
            
            #check answer match with question or not ?
            if int(qry_choice_exam.question_id) != int(args["question_quiz_id"]):
                return {"status": "input answer isn't in question"}, 403

        #check history_exam match with question
        history_exam = HistoriesExam.query.filter_by(status=True).filter_by(id=args["history_exam_id"]).first()
        quiz = Quizs.query.filter_by(status=True).filter_by(exam_id=history_exam.exam_id).first()
        question = QuestionsQuiz.query.filter_by(status=True).filter_by(id=args["question_quiz_id"]).first()
        if quiz.id != question.quiz_id:
            return {"status": "input question isn't match with quiz on history exam"}, 403

        #check input answer in one question is already in database or not
        correction_exam = CorrectionsExam.query.filter_by(history_exam_id=args["history_exam_id"]).filter_by(question_quiz_id=args["question_quiz_id"]).filter_by(status=True).first()
        qry_choice_exam = ChoicesQuiz.query.filter_by(id=args["answer_quiz_id"]).filter_by(status=True).first()
        
        if correction_exam is None:
            if args["answer_quiz_id"] is not None:
                choice = qry_choice_exam.is_correct
                result = CorrectionsExam(
                    args["history_exam_id"],
                    args["question_quiz_id"],
                    args["answer_quiz_id"],
                    choice,
                    True
                )
            else:
                choice = None
                result = CorrectionsExam(
                    args["history_exam_id"],
                    args["question_quiz_id"],
                    args["answer_quiz_id"],
                    choice,
                    True
                )

            db.session.add(result)
            db.session.commit()

            correction_exam = CorrectionsExam.query.get(result.id)

        else:
            if args["answer_quiz_id"] is not None:
                correction_exam.answer_quiz_id = args["answer_quiz_id"]
                correction_exam.is_correct = qry_choice_exam.is_correct
            else:
                {"status": "answer isn't be inputed"}, 403

            db.session.commit()

        #Calculation Score for Quiz
        #determine sum of question in quiz
        qry_exam = Exams.query.filter_by(id=qry_history_exam.exam_id).filter_by(status=True).first()
        qry_quiz = Quizs.query.filter_by(exam_id=qry_exam.id).filter_by(status=True).first()
        qry_question = QuestionsQuiz.query.filter_by(quiz_id=qry_quiz.id).filter_by(status=True).all()
    
        sum_question = len(qry_question)
        
        #determine answer true
        sum_true = 0
        qry_correction_exam = CorrectionsExam.query.filter_by(status=True).filter_by(history_exam_id=args["history_exam_id"]).all()
        for answer in qry_correction_exam:
            if answer.is_correct == True:
                sum_true += 1

        #calculate score
        score = round(sum_true * 100 / sum_question)
        
        #input score in history altatest
        qry_history_exam.score = score
        db.session.commit()

        correction_exam = marshal(correction_exam, CorrectionsExam.response_fields)

        name_answer = ChoicesQuiz.query.filter_by(id=correction_exam["answer_quiz_id"]).first()

        correction_exam["answer"] = name_answer.choice

        del correction_exam["is_correct"]
        del correction_exam["status"]
        del correction_exam["created_at"]
        del correction_exam["update_at"]

        return correction_exam, 200

    #Endpoint delete Correction Quiz by Id
    @mentee_required
    def delete(self, id):
        qry_correction_exam = CorrectionsExam.query.get(id)

        if qry_correction_exam is not None:
            db.session.delete(qry_correction_exam)
            db.session.commit()

            return {"status": "DELETED SUCCESS"}, 200

        return {"status": "NOT_FOUND"}, 404


class CorrectionsExamSubmit(Resource):
    # endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint to submit quiz question
    @mentee_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("history_exam_id", location="json", required=True)
        args = parser.parse_args()

        qry_history_exam = HistoriesExam.query.filter_by(status=True).filter_by(id=args["history_exam_id"]).first()
        if qry_history_exam is None:
            {"status": "History Exam in this Id isn't exist"}, 403

        qry_history_exam.is_complete = True

        db.session.commit()

        #get mentee_id by token
        verify_jwt_in_request()
        claims = get_jwt_claims()

        #get history subject
        exam_id = qry_history_exam.exam_id

        qry_exam = Exams.query.get(exam_id)

        qry_history_subject = HistoriesSubject.query.filter_by(status=True).filter_by(subject_id=qry_exam.subject_id).filter_by(mentee_id=claims["id"]).first()

        #get sum history_exam of mentee
        qry_history_exam_of_mentee = HistoriesExam.query.filter_by(status=True).filter_by(exam_id=exam_id).filter_by(mentee_id=claims["id"]).all()
        sum_history_exam_of_mentee = len(qry_history_exam_of_mentee)

        #fill result of exam to history_subject
        if qry_history_exam.score >= 80:
            qry_history_subject.score = qry_history_exam.score
            qry_history_subject.time_of_exam = sum_history_exam_of_mentee
            qry_history_subject.is_complete = True
            db.session.commit()
        else:
            qry_history_subject.score = qry_history_exam.score
            qry_history_subject.time_of_exam = sum_history_exam_of_mentee
            qry_history_subject.is_complete = False
            db.session.commit()

        qry_history_phase = HistoriesPhase.query.filter_by(status=True).filter_by(mentee_id=claims["id"]).all()
        
        # Make all modul and subject close when time of exam > 3
        if sum_history_exam_of_mentee >= 3 and qry_history_exam.score < 80:
            #delete all history_exam_of_mentee
            history_exam_of_mentee = HistoriesExam.query.filter_by(mentee_id=claims["id"]).all()
            for history_exam in history_exam_of_mentee:
                db.session.delete(history_exam)
                db.session.commit()

            for index_phase, history_phase in enumerate(qry_history_phase):
                #make all phase, is_complete and lock_key = False
                if index_phase == 0:
                    history_phase.is_complete = False
                    history_phase.lock_key = True
                else:
                    history_phase.is_complete = False
                    history_phase.lock_key = False

                phase = history_phase.phase_id
                qry_history_module = HistoriesModule.query.filter_by(status=True).filter_by(mentee_id=claims["id"]).all()
                histories_module = []
                for history_module in qry_history_module:
                    module = Modules.query.filter_by(status=True).filter_by(id=history_module.module_id).first()
                    if module.phase_id == phase:
                        histories_module.append(history_module)
                
                for index_module, history_module in enumerate(histories_module):
                    #make all modul, is_complete and lock_key = False
                    if index_module == 0 and index_phase == 0:
                        history_module.is_complete = False
                        history_module.lock_key = True
                    else:
                        history_module.is_complete = False
                        history_module.lock_key = False

                    module = history_module.module_id
                    qry_history_subject = HistoriesSubject.query.filter_by(status=True).filter_by(mentee_id=claims["id"]).all()
                    histories_subject = []
                    for history_subject in qry_history_subject:
                        subject = Subjects.query.filter_by(status=True).filter_by(id=history_subject.subject_id).first()
                        if subject.module_id == module:
                            histories_subject.append(history_subject)
                    
                    for index_subject, history_subject in enumerate(histories_subject):
                        #make all subject, is_complete and lock_key = False
                        if index_subject == 0 and index_module == 0 and index_phase == 0:
                            history_subject.is_complete = False
                            history_subject.lock_key = True
                            history_subject.score = 0
                            history_subject.time_of_exam = 0
                        else:
                            history_subject.is_complete = False
                            history_subject.lock_key = False
                            history_subject.score = 0
                            history_subject.time_of_exam = 0

            db.session.commit()

            respond = {"status" : "sudah 3x, ulangi dari awal"}

        elif sum_history_exam_of_mentee < 3 and qry_history_exam.score < 80:
            respond = {"status" : "belum lolos, coba lagi"}

        elif qry_history_exam.score > 80:
            #initial respond
            respond_subject = ""
            respond_modul = ""
            respond_phase = ""

            for index_phase, history_phase in enumerate(qry_history_phase):
                phase = history_phase.phase_id
                qry_history_module = HistoriesModule.query.filter_by(status=True).filter_by(mentee_id=claims["id"]).all()
                histories_module = []
                for history_module in qry_history_module:
                    module = Modules.query.filter_by(status=True).filter_by(id=history_module.module_id).first()
                    if module.phase_id == phase:
                        histories_module.append(history_module)
                
                for index_module, history_module in enumerate(qry_history_module):
                    module = history_module.module_id
                    qry_history_subject = HistoriesSubject.query.filter_by(status=True).filter_by(mentee_id=claims["id"]).all()
                    histories_subject = []
                    for history_subject in qry_history_subject:
                        subject = Subjects.query.filter_by(status=True).filter_by(id=history_subject.subject_id).first()
                        if subject.module_id == module:
                            histories_subject.append(history_subject)
                    
                    for index_subject, history_subject in enumerate(qry_history_subject):
                        #make lock_key true when is_complete of subject_id in the before is True
                        if history_subject.is_complete == True and index_subject != (len(qry_history_subject)-1):
                            qry_history_subject[index_subject+1].lock_key = True
                            respond_subject = {"status" : "lolos subject ini"}

                    #change lock_key in modul
                    if len(histories_subject) != 0:
                        modul_last_subject = histories_subject[-1]
                        if modul_last_subject.is_complete == True:
                            qry_history_module[index_module].is_complete = True
                            #input score in modul
                            sum_subject = len(histories_subject)
                            #calculate score
                            score_temporary = 0
                            for subject in histories_subject:
                                score_temporary += subject.score

                            score = round(score_temporary / sum_subject)

                            qry_history_module[index_module].score = score

                            # input lock_key in next modul
                            if index_module != (len(qry_history_module)-1):
                                qry_history_module[index_module+1].lock_key = True
                            
                            respond_modul = {"status" : "lolos modul ini"}

                #change lock key in phase
                if len(histories_module) != 0:
                    phase_last_modul = histories_module[-1]
                    if phase_last_modul.is_complete == True:
                        qry_history_phase[index_phase].certificate = "certificate-" + str(index_phase) + "-" + str(claims["full_name"])
                        #input score in phase
                        sum_module = len(histories_module)
                        #calculate score
                        score_temporary = 0
                        for module in histories_module:
                            score_temporary += module.score

                        score = round(score_temporary / sum_module)

                        qry_history_phase[index_module].score = score

                        # input lock_key in next phase
                        if index_phase != (len(qry_history_phase)-1):
                            qry_history_phase[index_phase+1].lock_key = True

                        respond_phase = {"status" : "lolos phase ini"}

            db.session.commit()

            if respond_phase != "":
                respond = respond_phase
            elif respond_modul != "":
                respond = respond_modul
            elif respond_subject != "":
                respond = respond_subject

        qry_history_subject = HistoriesSubject.query.filter_by(status=True).filter_by(subject_id=qry_exam.subject_id).filter_by(mentee_id=claims["id"]).first()

        # return marshal(qry_history_subject, HistoriesSubject.response_fields), 200
        return respond, 200

api.add_resource(CorrectionsExamResource, "", "/<id>")
api.add_resource(CorrectionsExamSubmit, "", "/submit")