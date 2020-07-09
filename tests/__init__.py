import pytest
import json
import logging
from flask import Flask, request, json
from blueprints import app, cache, db

from blueprints.admin.model import Admins
from blueprints.mentee.model import Mentees

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

    #inser user data
<<<<<<< HEAD
    admin = Admins(username='umam12', password=hash_pass, full_name='Ismanul Umam', role='super', email='pangestuahmadaji@gmail.com', address='Malang, East Java', phone='0856473242', place_birth='Malang', date_birth='3 Maret 1993', avatar='https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/avatar/ddaf4321fe364955899e2f4f37170523_8i9fvU3+-+Imgur.jpg', github='https://github.com/ahmadajip55', description="Lorem Ipsum Doler", salt=salt, status=True)
    mentee = Mentees(username="rosliani12", password=hash_pass, full_name="Yopi Ragil", email="yopi@alterra.id", address="Klaten, East Java", phone='0856473241', place_birth="Klaten", date_birth="2 Maret 1995", avatar="https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/avatar/8023d583899a4ed4a22bd01e35777525_DSC02275.JPG", background_education="Fisika", github="https://github.com/ahmadajip5", description="Lorem Ipsum Doler 2", salt=salt, status=True)
=======
    admin = Admins(username='umam12', password=hash_pass, full_name='Ismanul Umam', role='super', email='umam@gmail.com', address='Malang, East Java', phone="0856473242", place_birth='Malang', date_birth='3 Maret 1993', avatar='https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/avatar/ddaf4321fe364955899e2f4f37170523_8i9fvU3+-+Imgur.jpg', github='https://github.com/ahmadajip55', description="Lorem Ipsum Doler", salt=salt, status=True)
>>>>>>> 88ad2993b973a9ca66d40ffcbcd2e24386e6a47d
    db.session.add(admin)
    db.session.commit()

    mentee = Mentees(username="rosliani12", password=hash_pass, full_name="Yopi Ragil", email="yopi@gmail.com", address="Klaten, East Java", phone="0856473241", place_birth="Klaten", date_birth="2 Maret 1995", avatar="https://alterra-online-learning.s3-ap-southeast-1.amazonaws.com/avatar/8023d583899a4ed4a22bd01e35777525_DSC02275.JPG", background_education="Fisika", github="https://github.com/ahmadajip5", description="Lorem Ipsum Doler 2", salt=salt, status=True)
    db.session.add(mentee)
    db.session.commit()    
    
    # phase = Phases(name="phase 1", description="coba deskripsi", status=True)
    # db.session.add(phase)
    # db.session.commit()

    # modul = Modules(admin_id= 1, phase_id=1, name="Python", description="coba deskripsi modul", image="www.module.jsdhsd.jpg", status=True)
    # db.session.add(modul)
    # db.session.commit()

    # review_module = ReviewsModule(mentee_id=1, module_id=1, content="ini contentnya", score=1, status=True)
    # db.session.add(review_module)
    # db.session.commit()

    # requirement_module =RequirementsModule(module_id=1, description="coba deskripsi ini", status=True )
    # db.session.add(requirement_module)
    # db.session.commit()

    # subject = Subjects(module_id= 1, name="algorithm", description="coba deskripsi subject", quesioner="www.ksjjsd.com", status=True)
    # db.session.add(subject)
    # db.session.commit()

    # file_subject = FilesSubject(subject_id=1, name="nama file", content_file="www.link.com.jpg", category_file="presentation", status=True )
    # db.session.add(file_subject)
    # db.session.commit()

    # exam = Exams(subject_id=1, type_exam="quiz", status= True)
    # db.session.add(exam)
    # db.session.commit()

    # live_code = Livecodes(exam_id=1, name="ujian", description="deskripsi ujiannya", link="www.linknya.ini", status=True)
    # db.session.add(live_code)
    # db.session.commit()

    # quiz = Quizs(exam_id=1, name="ini quiznya", description="deskripsinya ini", status=True)
    # db.session.add(quiz)
    # db.session.commit()

    # question_quiz = QuestionsQuiz(quiz_id=1, question="coba sebutkan apa saja?", status: True)
    # db.session.add(question_quiz)
    # db.session.commit()

    # choice_quiz = ChoicesQuis (question_id = 1, choice="jaya wijaya", is_correct=True, status=True)
    # db.session.add(choice_quiz)
    # db.session.commit()

    # altatest = Altatests(question_sum = 1, status=True)
    # db.session.add(altatest)
    # db.session.commit()

    # question_altatest = QuestionsAltatest(admin_id=1, question="ini pertanyaannya lalu jawabannya apa?", status=True)
    # db.session.add(question_altatest)
    # db.session.commit()

    # choice_altatest = ChoicesAltatest(question_id=1, choice="ini jawabannya", is_correct=True, status=True)
    # db.session.add(choice_altatest)
    # db.session.commit()

    # detail_altatest = DetailsAltatest(altatest_id = 1, question_id=1, status=True)
    # db.session.add(detail_altatest)
    # db.session.commit()

    # history_altatest=HistoriesAltatest(altatest_id=1, mentee_id=1, score=50, time_start="2020-07-03 08:15:09", is_commplete=True, status=True) 
    # db.session.add(history_altatest)
    # db.session.commit()

    # correction_altatest = CorrectionsAltatest(history_altatest_id=1, question_altatest_id=1, answer_id=1, is_correct=True, status=True )
    # db.session.add(correction_altatest)
    # db.session.commit()

    # history_phase = HistoriesPhase(phase_id=1, mentee_id=1, score=85, certificate="alta-phase-1-aji-20-10-20", lock_key=True, status=True)
    # db.session.add(history_phase)
    # db.session.commit()

    # history_module= HistoriesModule(module_id=1, mentee_id=1, score=90, is_commplete=True, lock_key=True, status=True)
    # db.session.add(history_module)
    # db.session.commit()

    # history_subject= HistoriesSubject(subject_id=1, mentee_id=1, score=90, time_of_exam, is_commplete, lock_key=True, status=True)
    # db.session.add(history_subject)
    # db.session.commit()

    # history_exam = HistoriesExam(exam_id=1, mentee_id=1, score=90, is_commplete=True, status=True)
    # db.session.add(history_exam)
    # db.session.commit()

    # correction_exam = CorrectionsExam(history_exam_id=1, question_quiz_id=1, answer_quiz_id=1, is_correct=True, status=True)
    # db.session.add(correction_exam)
    # db.session.commit()

    # yield db
    # db.drop_all()

def create_token_admin():
    token = cache.get("test-token-admin")
    if token is None:
        data = {
            'username': 'umam12',
            'password': 'password'
        }

        req = call_client(request)
<<<<<<< HEAD
        res = req.post('/auth/admin', data=json.dumps(data))
=======
        res = req.post('/auth/admin', data=json.dumps(data), content_type="application/json")
>>>>>>> 88ad2993b973a9ca66d40ffcbcd2e24386e6a47d

        res_json = json.loads(res.data)
        logging.warning('RESULT:%s', res_json)

        assert res.status_code == 200

        cache.set('test-token-admin', res_json['token'], timeout=60)
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
<<<<<<< HEAD
        res = req.post('/auth/mentee', data=json.dumps(data), content)
=======
        res = req.post('/auth/mentee', data=json.dumps(data), content_type="application/json")
>>>>>>> 88ad2993b973a9ca66d40ffcbcd2e24386e6a47d

        res_json = json.loads(res.data)
        logging.warning('RESULT:%s', res_json)

        assert res.status_code == 200

        cache.set('test-token-mentee', res_json['token'], timeout=60)
        return res_json['token']
    
    else:
        return token