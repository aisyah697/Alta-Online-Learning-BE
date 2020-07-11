import json 
from . import app, client, cache, create_token_admin, create_token_mentee, create_token_admin_academic, create_token_admin_business, create_token_admin_council,init_database

class TestExamCrud():
    def test_exam_get_by_id(self, client, init_database):
        token = create_token_admin()
        res = client.get('/exam/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_exam_get_by_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.get('/exam/100', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_exam_get_by_id_not_super_academic(self, client, init_database):
        token = create_token_admin_council()
        res = client.get('/exam/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_exam_post(self, client, init_database):
        token = create_token_admin()
        data={
            "subject_id": 2,
            "type_exam": "quiz",
            "status": True
        }
        res = client.post('/exam', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_exam_post_admin_business(self, client, init_database):
        token = create_token_admin_business()
        data={
            "subject_id": 1,
            "type_exam": "quiz",
            "status": True
        }
        res = client.post('/exam', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_exam_post_subject_id_not_found(self, client, init_database):
        token = create_token_admin()
        data={
            "subject_id": 3,
            "type_exam": "quiz",
            "status": True
        }
        res = client.post('/exam', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404