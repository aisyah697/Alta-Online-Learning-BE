import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app
from sqlalchemy import desc
from  sqlalchemy.sql.expression import func, select
from datetime import datetime
from flask_jwt_extended import (
    JWTManager,
    get_jwt_identity,
    verify_jwt_in_request,
    jwt_required,
    get_jwt_claims,
)
from blueprints import mentee_required, admin_required

from .model import HistoriesAltatest
from ..correction_altatest.model import CorrectionsAltatest
from ..mentee.model import Mentees
from ..altatest.model import Altatests
from ..detail_altatest.model import DetailsAltatest
from ..question_altatest.model import QuestionsAltatest
from ..choice_altatest.model import ChoicesAltatest

bp_history_altatest = Blueprint("history_altatest", __name__)
api = Api(bp_history_altatest)


class HistoriesAltatestResource(Resource):
    # endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    # endpoint for get history altatest by ID
    @mentee_required
    def get(self, id=None):
        #get id mentee for filter history altatest
        verify_jwt_in_request()
        claims = get_jwt_claims()

        qry_history_altatest = HistoriesAltatest.query.filter_by(status=True).filter_by(mentee_id=claims["id"]).first()

        if qry_history_altatest is not None:
            history_altatest = marshal(qry_history_altatest, HistoriesAltatest.response_fields)
            
            qry_altatest = Altatests.query.filter_by(status=True).filter_by(id=history_altatest["altatest_id"]).first()

            if qry_altatest is not None:
                qry_detail_question = DetailsAltatest.query.filter_by(status=True).filter_by(altatest_id=qry_altatest.id).all()
                rows = []
                for question in qry_detail_question:
                    arrays = []
                    qry_choice = ChoicesAltatest.query.filter_by(status=True).filter_by(question_id=question.question_id).all()
                    for choice in qry_choice:
                        choice = marshal(choice, ChoicesAltatest.response_fields)
                        choice["history_altatest_id"] = qry_history_altatest.id
                        arrays.append(choice)
                    
                    question_altatest = marshal(QuestionsAltatest.query.get(question.question_id), QuestionsAltatest.response_fields)
                    
                    question_altatest["history_altatest_id"] = qry_history_altatest.id
                    question_altatest["choice"] = arrays

                    rows.append(question_altatest)

                altatest = marshal(qry_altatest, Altatests.response_fields)
                altatest["question"] = rows

                history_altatest["altatest"] = altatest

                return history_altatest, 200
            
            return {"status": "Id Altatest is not found"}, 404

        return {"status": "Id History Altatest is not found"}, 404

    # endpoint post history altatest
    @mentee_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("question_sum", location="json", default=25)
        parser.add_argument("status", location="json", type=bool, default=True)
        args = parser.parse_args()

        #check mentee already register for altatest or not
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        qry_history_altatest = HistoriesAltatest.query.filter_by(mentee_id=claims["id"]).first()
        if qry_history_altatest is not None:
            return {"status": "Mentee Already register for Altatest"}, 403

        result = Altatests(
            args["question_sum"],
            args["status"]
        )

        db.session.add(result)
        db.session.commit()
  
        #check id altatest
        qry_altatest = Altatests.query.filter_by(status=True).filter_by(id=result.id).first()
        altatest = marshal(qry_altatest, Altatests.response_fields)

        if qry_altatest is None:
            return {"status": "Altatest is Not Found"}, 404
        
        score = None
        is_complete = None
        status =  True
        
        #get mentee_id from id authentification
        verify_jwt_in_request()
        claims = get_jwt_claims()

        result = HistoriesAltatest(
            altatest["id"],
            claims["id"],
            score,
            is_complete,
            status
        )

        db.session.add(result)
        db.session.commit()

        qry_question = QuestionsAltatest.query.filter_by(status=True).order_by(func.rand()).limit(args["question_sum"])
        rows = []
        for question in qry_question:
            detail = DetailsAltatest(
                altatest["id"],
                question.id, 
                True
            )

            db.session.add(detail)
            db.session.commit()

        #show respond after post
        qry_history_altatest = HistoriesAltatest.query.filter_by(status=True).filter_by(id=result.id).first()
        history_altatest = marshal(qry_history_altatest, HistoriesAltatest.response_fields)

        qry_detail_question = DetailsAltatest.query.filter_by(status=True).filter_by(altatest_id=qry_altatest.id).all()
        rows = []
        for question in qry_detail_question:
            arrays = []
            qry_choice = ChoicesAltatest.query.filter_by(status=True).filter_by(question_id=question.question_id).order_by(func.rand()).all()
            
            for choice in qry_choice:
                choice = marshal(choice, ChoicesAltatest.response_fields)
                choice["history_altatest_id"] = qry_history_altatest.id
                arrays.append(choice)
 
            question_altatest = marshal(QuestionsAltatest.query.get(question.question_id), QuestionsAltatest.response_fields)
            
            question_altatest["history_altatest_id"] = qry_history_altatest.id
            question_altatest["choice"] = arrays

            rows.append(question_altatest)

        altatest["question"] = rows

        history_altatest["altatest"] = altatest

        return history_altatest, 200

    #endpoint for soft delete
    def put(self, id):
        #check id in query or not
        qry_history_altatest = HistoriesAltatest.query.get(id)
        
        if qry_history_altatest is None:
            return {'status': 'History Altatest is NOT_FOUND'}, 404
        
        #input update status for soft delete
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete      
        qry_history_altatest.status = args['status']

        db.session.commit()

        return marshal(qry_history_altatest, HistoriesAltatest.response_fields), 200

    #endpoint for change score
    @jwt_required
    def patch(self):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()

        #check id in query or not
        qry_history_altatest = HistoriesAltatest.query.filter_by(mentee_id=claims["id"]).first()

        if qry_history_altatest is None:
            return {'status': 'History Altatest is NOT_FOUND'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument("is_complete", location="json", help='invalid status', choices=("start", "end", "null"))
        args = parser.parse_args()

        if args["is_complete"] == "start":
            qry_history_altatest.is_complete = args["is_complete"]

            qry_history_altatest.time_start = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.session.commit()
        
        elif args["is_complete"] == "end":
            qry_history_altatest.is_complete = args["is_complete"]
            db.session.commit()
        
        else:
            qry_history_altatest.is_complete = None
            db.session.commit()

        return marshal(qry_history_altatest, HistoriesAltatest.response_fields), 200


    #Endpoint delete history Altatest by Id
    def delete(self, id):
        history_altatest = HistoriesAltatest.query.get(id)

        if history_altatest is not None:
            db.session.delete(history_altatest)
            db.session.commit()

            return {"status": "DELETED SUCCESS"}, 200

        return {"status": "NOT_FOUND"}, 404


class HistoriesAltatestAll(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint to get all and sort by score and created_at
    @admin_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=("score", "created_at"))
        parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry_history_altatest = HistoriesAltatest.query

        if args["orderby"] is not None:
            if args['orderby'] == "score":
                if args["sort"] == "desc":
                    qry_history_altatest = qry_history_altatest.order_by(desc(HistoriesAltatest.score))
                else:
                    qry_history_altatest = qry_history_altatest.order_by(HistoriesAltatest.score)
            elif args["orderby"] == "created_at":
                if args["sort"] == "desc":
                    qry_history_altatest = qry_history_altatest.order_by(desc(HistoriesAltatest.created_at))
                else:
                    qry_history_altatest = qry_history_altatest.order_by(HistoriesAltatest.created_at)

        rows = []
        for row in qry_history_altatest.limit(args['rp']).offset(offset).all():
            if row.status == True:
                row = marshal(row, HistoriesAltatest.response_fields)
                rows.append(row)

        return rows, 200


class HistoriesCorrectionQuestion(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint to correction question of altatest and calculate score, then input on database alatatest
    @mentee_required
    def post(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument("history_altatest_id", location="json", required=True)
        parser.add_argument("question_altatest_id", location="json", required=True)
        parser.add_argument("answer_id", location="json", default=None)
        args = parser.parse_args()

        #check input history_altatest in database there or not
        qry_history_altatest = HistoriesAltatest.query.filter_by(id=args["history_altatest_id"]).filter_by(status=True).first()
        if qry_history_altatest is None:
            return {"status": "input history_altatest isn't in database"}, 403

        #check mentee from token match with mentee from history_altatest
        verify_jwt_in_request()
        claims = get_jwt_claims()

        if claims["id"] != qry_history_altatest.mentee_id:
            return {"status": "mentee in token and history_altatest isn't match"}, 403

        #check input question is in database or not
        qry_question_altatest = QuestionsAltatest.query.filter_by(id=args["question_altatest_id"]).filter_by(status=True).first()
        if qry_question_altatest is None:
            return {"status": "input question isn't in database"}, 403

        #check input answer isn't at database
        if args["answer_id"] is not None:
            qry_choice_altatest = ChoicesAltatest.query.filter_by(id=args["answer_id"]).filter_by(status=True).first()
            if qry_choice_altatest is None:
                return {"status": "input answer isn't in database"}, 403

        #check answer match with question or not?
        if args["answer_id"] is not None:
            answer = ChoicesAltatest.query.filter_by(id=args["answer_id"]).filter_by(status=True).first()
            if int(answer.question_id) != int(args["question_altatest_id"]):
                return {"status": "input answer isn't in question"}, 403

        #check input answer in one question is already there in database 
        correction_altatest = CorrectionsAltatest.query.filter_by(history_altatest_id=args["history_altatest_id"]).filter_by(question_altatest_id=args["question_altatest_id"]).filter_by(status=True).first()
        qry_choice_altatest = ChoicesAltatest.query.filter_by(id=args["answer_id"]).filter_by(status=True).first()
        
        if correction_altatest is None:    
            if args["answer_id"] is not None:
                choice = qry_choice_altatest.is_correct

                result = CorrectionsAltatest(
                    args["history_altatest_id"],
                    args["question_altatest_id"],
                    args["answer_id"],
                    choice,
                    True
                )
            else:
                choice = None
                result = CorrectionsAltatest(
                    args["history_altatest_id"],
                    args["question_altatest_id"],
                    args["answer_id"],
                    choice,
                    True
                )

            db.session.add(result)
            db.session.commit()

            correction_altatest = CorrectionsAltatest.query.get(result.id)
        
        else:
            if args["answer_id"] is not None:
                correction_altatest.answer_id = args["answer_id"]
                correction_altatest.is_correct = qry_choice_altatest.is_correct
            else:
                {"status": "answer isn't be inputed"}, 403

            db.session.commit()

        #Calculation Score for Altatest
        #determine sum of question
        qry_altatest = Altatests.query.filter_by(id=qry_history_altatest.altatest_id).filter_by(status=True).first()
        qry_question = DetailsAltatest.query.filter_by(altatest_id=qry_altatest.id).filter_by(status=True).all()
        sum_question = len(qry_question)

        #determine answer true
        sum_true = 0
        qry_correction_altatest = CorrectionsAltatest.query.filter_by(status=True).filter_by(history_altatest_id=args["history_altatest_id"]).all()
        for answer in qry_correction_altatest:
            if answer.is_correct == True:
                sum_true += 1

        #calculate score
        score = round(sum_true * 100 / sum_question)
        
        #input score in history altatest
        qry_history_altatest.score = score
        db.session.commit()

        correction_altatest = marshal(correction_altatest, CorrectionsAltatest.response_fields)

        name_answer = ChoicesAltatest.query.filter_by(id=correction_altatest["answer_id"]).first()

        correction_altatest["answer"] = name_answer.choice

        del correction_altatest["is_correct"]
        del correction_altatest["status"]
        del correction_altatest["created_at"]
        del correction_altatest["update_at"]

        return correction_altatest, 200


class HistoriesAltatestAllStatus(Resource):
    #for solve cors
    def option(self, id=None):
        return {"status": "ok"}, 200
        
    #endpoint to get all status of history altatest 
    def get(self):
        qry_history_altatest = HistoriesAltatest.query

        rows = []
        for row in qry_history_altatest:
            row = marshal(row, HistoriesAltatest.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200


api.add_resource(HistoriesAltatestResource, "", "/<id>")
api.add_resource(HistoriesAltatestAll, "", "/mentee")
api.add_resource(HistoriesAltatestAllStatus, "", "/all")
api.add_resource(HistoriesCorrectionQuestion, "", "/question")