import pytest
import json
import logging
from flask import Flask, request, json
from blueprints import app, cache, db
from datetime import datetime

from blueprints.admin.model import Admins
from blueprints.mentee.model import Mentees
from blueprints.question_altatest.model import QuestionsAltatest
from blueprints.choice_altatest.model import ChoicesAltatest
from blueprints.altatest.model import Altatests
from blueprints.history_altatest.model import HistoriesAltatest
from blueprints.detail_altatest.model import DetailsAltatest
from blueprints.correction_altatest.model import CorrectionsAltatest
from blueprints.phase.model import Phases
from blueprints.module.model import Modules
from blueprints.review_module.model import ReviewsModule
from blueprints.requirement_module.model import RequirementsModule
from blueprints.subject.model import Subjects
from blueprints.file_subject.model import FilesSubject
from blueprints.exam.model import Exams
from blueprints.livecode.model import Livecodes
from blueprints.quiz.model import Quizs
from blueprints.question_quiz.model import QuestionsQuiz
from blueprints.choice_quiz.model import ChoicesQuiz
from blueprints.correction_exam.model import CorrectionsExam
from blueprints.history_subject.model import HistoriesSubject
from blueprints.history_exam.model import HistoriesExam
from blueprints.history_module.model import HistoriesModule
from blueprints.history_phase.model import HistoriesPhase

import uuid, hashlib
from sqlalchemy.sql import func

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

@pytest.fixture
def init_database():
    #create database & table
    db.drop_all()
    db.create_all()

    salt = uuid.uuid4().hex
    encoded = ('%s%s' % ('password', salt)).encode('utf-8')
    hash_pass = hashlib.sha512(encoded).hexdigest()

    # encoded2 = ('%s%s' % ('mentee', salt)).encode('utf-8')
    # hash_pass2 = hashlib.sha512(encoded2).hexdigest()

    #insert user data
    admin_super = Admins(username='umam12', password=hash_pass, full_name='Ismanul Umam', role='super', email='umam@gmail.com', address='Malang, East Java', phone="0856473242", place_birth='Malang', date_birth='3 Maret 1993', avatar='https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/avatar/ddaf4321fe364955899e2f4f37170523_8i9fvU3+-+Imgur.jpg', github='https://github.com/ahmadajip55', description="Lorem Ipsum Doler", salt=salt, status=True)
    admin_academic = Admins(username='kobar12', password=hash_pass, full_name='Kobar Septyanus', role='academic', email='umam@gmail.com', address='Malang, East Java', phone="0856473242", place_birth='Malang', date_birth='3 Maret 1993', avatar='https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/avatar/ddaf4321fe364955899e2f4f37170523_8i9fvU3+-+Imgur.jpg', github='https://github.com/ahmadajip55', description="Lorem Ipsum Doler", salt=salt, status=True)
    admin_council = Admins(username='yovan12', password=hash_pass, full_name='Yovan Pranandya', role='council', email='umam@gmail.com', address='Malang, East Java', phone="0856473242", place_birth='Malang', date_birth='3 Maret 1993', avatar='https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/avatar/ddaf4321fe364955899e2f4f37170523_8i9fvU3+-+Imgur.jpg', github='https://github.com/ahmadajip55', description="Lorem Ipsum Doler", salt=salt, status=True)
    admin_business = Admins(username='bram12', password=hash_pass, full_name='Bram Pangestu', role='business', email='umam@gmail.com', address='Malang, East Java', phone="0856473242", place_birth='Malang', date_birth='3 Maret 1993', avatar='https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/avatar/ddaf4321fe364955899e2f4f37170523_8i9fvU3+-+Imgur.jpg', github='https://github.com/ahmadajip55', description="Lorem Ipsum Doler", salt=salt, status=True)
    db.session.add(admin_super)
    db.session.add(admin_academic)
    db.session.add(admin_council)
    db.session.add(admin_business)
    db.session.commit()

    mentee_1 = Mentees(username="rosliani12", password=hash_pass, full_name="Yopi Ragil", email="yopi@gmail.com", address="Klaten, East Java", phone="0856473241", place_birth="Klaten", date_birth="2 Maret 1995", avatar="https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/avatar/8023d583899a4ed4a22bd01e35777525_DSC02275.JPG", background_education="Fisika", github="https://github.com/ahmadajip5", description="Lorem Ipsum Doler 2", salt=salt, status=True)
    mentee_2 = Mentees(username="aisyah12", password=hash_pass, full_name="Aisyah", email="yopi@gmail.com", address="Klaten, East Java", phone="08564732412", place_birth="Klaten", date_birth="2 Maret 1995", avatar="https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/avatar/8023d583899a4ed4a22bd01e35777525_DSC02275.JPG", background_education="Fisika", github="https://github.com/ahmadajip5", description="Lorem Ipsum Doler 2", salt=salt, status=True)
    db.session.add(mentee_1)
    db.session.add(mentee_2)
    db.session.commit()    
    
    phase = Phases(name="phase 1", description="coba deskripsi", status=True)
    db.session.add(phase)
    db.session.commit()

    modul = Modules(admin_id= 1, phase_id=1, name="Python", description="coba deskripsi modul", image="www.module.jsdhsd.jpg", status=True)
    db.session.add(modul)
    db.session.commit()

    review_module = ReviewsModule(mentee_id=1, module_id=1, content="ini contentnya", score=1, status=True)
    db.session.add(review_module)
    db.session.commit()

    requirement_module =RequirementsModule(module_id=1, description="coba deskripsi ini", status=True )
    db.session.add(requirement_module)
    db.session.commit()

    subject_1 = Subjects(module_id= 1, name="algorithm", description="coba deskripsi subject", quesioner="www.ksjjsd.com", status=True)
    subject_2 = Subjects(module_id= 1, name="structure data", description="coba deskripsi subject", quesioner="www.ksjjsd.com", status=True)
    db.session.add(subject_1)
    db.session.add(subject_2)
    db.session.commit()

    file_subject = FilesSubject(subject_id=1, name="nama file", content_file="www.link.com.jpg", category_file="presentation", status=True )
    db.session.add(file_subject)
    db.session.commit()

    exam = Exams(subject_id=1, type_exam="quiz", status= True)
    db.session.add(exam)
    db.session.commit()

    live_code = Livecodes(exam_id=1, name="ujian", description="deskripsi ujiannya", link="www.linknya.ini", status=True)
    db.session.add(live_code)
    db.session.commit()

    quiz = Quizs(exam_id=1, name="ini quiznya", description="deskripsinya ini", status=True)
    db.session.add(quiz)
    db.session.commit()

    question_quiz = QuestionsQuiz(quiz_id=1, question="coba sebutkan apa saja?", status= True)
    db.session.add(question_quiz)
    db.session.commit()

    choice_quiz = ChoicesQuiz (question_id = 1, choice="jaya wijaya", is_correct=True, status=True)
    choice_quiz1 = ChoicesQuiz (question_id = 1, choice="merapi", is_correct=False, status=True)
    db.session.add(choice_quiz)
    db.session.add(choice_quiz1)
    db.session.commit()

    altatest = Altatests(question_sum = 1, status=True)
    db.session.add(altatest)
    db.session.commit()

    question_altatest = QuestionsAltatest(admin_id=1, question="ini pertanyaannya lalu jawabannya apa?", status=True)
    db.session.add(question_altatest)
    db.session.commit()

    choice_altatest = ChoicesAltatest(question_id=1, choice="ini jawabannya", is_correct=True, status=True)
    db.session.add(choice_altatest)
    db.session.commit()

    detail_altatest = DetailsAltatest(altatest_id = 1, question_id=1, status=True)
    db.session.add(detail_altatest)
    db.session.commit()

    history_altatest = HistoriesAltatest(altatest_id=1, mentee_id=1, score=50, time_start=datetime.now(), is_complete=True, status=True) 
    db.session.add(history_altatest)
    db.session.commit()

    correction_altatest = CorrectionsAltatest(history_altatest_id=1, question_altatest_id=1, answer_id=1, is_correct=True, status=True )
    db.session.add(correction_altatest)
    db.session.commit()

    history_phase = HistoriesPhase(phase_id=1, mentee_id=1, score=85, certificate="alta-phase-1-aji-20-10-20", date_certificate=datetime.now(),lock_key=True, status=True)
    db.session.add(history_phase)
    db.session.commit()

    history_module= HistoriesModule(module_id=1, mentee_id=1, score=90, is_complete=True, lock_key=True, status=True)
    db.session.add(history_module)
    db.session.commit()

    history_subject= HistoriesSubject(subject_id=1, mentee_id=1, score=90, time_of_exam=1, is_complete=False, lock_key=True, status=True)
    db.session.add(history_subject)
    db.session.commit()

    history_exam = HistoriesExam(exam_id=1, mentee_id=1, score=90, is_complete=True, status=True)
    db.session.add(history_exam)
    db.session.commit()

    correction_exam = CorrectionsExam(history_exam_id=1, question_quiz_id=1, answer_quiz_id=1, is_correct=True, status=True)
    db.session.add(correction_exam)
    db.session.commit()

    yield db
    db.drop_all()

def create_token_admin():
    token = cache.get("test-token-admin")
    if token is None:
        data = {
            'username': 'umam12',
            'password': 'password'
        }

        req = call_client(request)
        res = req.post('/auth/admin', data=json.dumps(data), content_type="application/json")

        res_json = json.loads(res.data)
        logging.warning('RESULT:%s', res_json)

        assert res.status_code == 200

        cache.set('test-token-admin', res_json['token'], timeout=60)
        return res_json['token']
    
    else:
        return token

def create_token_admin_academic():
    token = cache.get("test-token-admin-academic")
    if token is None:
        data = {
            'username': 'kobar12',
            'password': 'password'
        }

        req = call_client(request)
        res = req.post('/auth/admin', data=json.dumps(data), content_type="application/json")

        res_json = json.loads(res.data)
        logging.warning('RESULT:%s', res_json)

        assert res.status_code == 200

        cache.set('test-token-admin-academic', res_json['token'], timeout=60)
        return res_json['token']
    
    else:
        return token

def create_token_admin_council():
    token = cache.get("test-token-admin-council")
    if token is None:
        data = {
            'username': 'yovan12',
            'password': 'password'
        }

        req = call_client(request)
        res = req.post('/auth/admin', data=json.dumps(data), content_type="application/json")

        res_json = json.loads(res.data)
        logging.warning('RESULT:%s', res_json)

        assert res.status_code == 200

        cache.set('test-token-admin-council', res_json['token'], timeout=60)
        return res_json['token']
    
    else:
        return token

def create_token_admin_business():
    token = cache.get("test-token-admin-business")
    if token is None:
        data = {
            'username': 'bram12',
            'password': 'password'
        }

        req = call_client(request)
        res = req.post('/auth/admin', data=json.dumps(data), content_type="application/json")

        res_json = json.loads(res.data)
        logging.warning('RESULT:%s', res_json)

        assert res.status_code == 200

        cache.set('test-token-admin-business', res_json['token'], timeout=60)
        return res_json['token']
    
    else:
        return token

def create_token_mentee():
    token = cache.get("test-token-mentee")
    if token is None:
        data = {
            "username": "rosliani12",
            "password": "password"
        }

        req = call_client(request)
        res = req.post('/auth/mentee', data=json.dumps(data), content_type="application/json")

        res_json = json.loads(res.data)
        logging.warning('RESULT:%s', res_json)

        assert res.status_code == 200

        cache.set('test-token-mentee', res_json['token'], timeout=60)
        return res_json['token']
    
    else:
        return token

def create_token_mentee_user():
    token = cache.get("test-token-mentee-user")
    if token is None:
        data = {
            "username": "aisyah12",
            "password": "password"
        }

        req = call_client(request)
        res = req.post('/auth/mentee', data=json.dumps(data), content_type="application/json")

        res_json = json.loads(res.data)
        logging.warning('RESULT:%s', res_json)

        assert res.status_code == 200

        cache.set('test-token-mentee-user', res_json['token'], timeout=60)
        return res_json['token']
    
    else:
        return token