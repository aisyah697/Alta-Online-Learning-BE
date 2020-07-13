import json 
from . import app, client, cache, create_token_admin, create_token_mentee, create_token_mentee_user, create_token_admin_academic, create_token_admin_business, create_token_admin_council,init_database

class TestCorrectionExam():
    def test_post_correction_exam(self, client, init_database):
        token=create_token_mentee()
        data={
            "history_exam_id": 1,
            "question_quiz_id": 1,
            "answer_quiz_id": 1
            }
        res = client.post('/correctionexam', data=json.dumps(data),  headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200 

    def test_post_correction_exam_historyexam_none(self, client, init_database):
        token=create_token_mentee()
        data={
            "history_exam_id": 10,
            "question_quiz_id": 1,
            "answer_quiz_id": 1
            }
        res = client.post('/correctionexam', data=json.dumps(data),  headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 403

    def test_post_correction_exam_token_not_match(self, client, init_database):
        token=create_token_mentee_user()
        data={
            "history_exam_id": 1,
            "question_quiz_id": 1,
            "answer_quiz_id": 2
            }
        res = client.post('/correctionexam', data=json.dumps(data),  headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 403

    def test_get_correction_exam_by_id(self, client, init_database):
        token = create_token_mentee()
        data={
            "question_quiz_id": 1,
            }
        res = client.get('/correctionexam',data=json.dumps(data), headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_correction_exam_by_id_not_found(self, client, init_database):
        token = create_token_mentee()
        data={
            "question_quiz_id": 9,
            }
        res = client.get('/correctionexam',data=json.dumps(data), headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    def test_post_correction_exam_by_id(self, client, init_database):
        token = create_token_mentee()
        data={
            "history_exam_id": 1,
            }
        res = client.post('/correctionexam/submit',data=json.dumps(data), headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_post_correction_exam_by_id_history_exam_not_found(self, client, init_database):
        token = create_token_mentee()
        data={
            "history_exam_id": 100,
            }
        res = client.post('/correctionexam/submit',data=json.dumps(data), headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 403

    def test_delete_correction_exam(self, client, init_database):
        token = create_token_mentee()
        res = client.delete('/correctionexam/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_delete_correction_exam_not_found(self, client, init_database):
        token = create_token_mentee()
        res = client.delete('/correctionexam/100', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404