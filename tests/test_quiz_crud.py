import json 
from . import app, client, cache, create_token_admin, create_token_mentee, create_token_admin_academic, create_token_admin_business, create_token_admin_council,init_database

class TestQuizCrud():
    def test_quiz_get_by_id(self, client, init_database):
        token = create_token_admin()
        res = client.get('/quiz/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_quiz_get_by_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.get('/quiz/100', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_quiz_get_by_id_admin_business(self, client, init_database):
        token = create_token_admin_business()
        res = client.get('/quiz/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_quiz_post(self, client, init_database):
        token = create_token_admin()
        data={
            "exam_id": 3,
            "name": "Lorem Ipsum Dolor",
            "description": "Quiz ini adalah blablabla",
            "status": True
        }
        res = client.post('/quiz', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_quiz_post_admin_business(self, client, init_database):
        token = create_token_admin_business()
        data={
            "exam_id": 1,
            "name": "Lorem Ipsum Dolor",
            "description": "Quiz ini adalah blablabla",
            "status": True
        }
        res = client.post('/quiz', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_quiz_post_exam_id_not_found(self, client, init_database):
        token = create_token_admin()
        data={
            "exam_id": 100,
            "name": "Lorem Ipsum Dolor",
            "description": "Quiz ini adalah blablabla",
            "status": True
        }
        res = client.post('/quiz', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_quiz_post_exam_id_have_another_quiz(self, client, init_database):
        token = create_token_admin()
        data={
            "exam_id": 1,
            "name": "Lorem Ipsum Dolor",
            "description": "Quiz ini adalah blablabla",
            "status": True
        }
        res = client.post('/quiz', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_quiz_put(self, client, init_database):
        token = create_token_mentee()
        data = {
            "status": True
        }
        res = client.put('/quiz/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_quiz_put_id_not_found(self, client, init_database):
        token = create_token_mentee()
        data = {
            "status": True
        }
        res = client.put('/quiz/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_quiz_patch(self, client, init_database):
        token = create_token_admin()
        data = {
            "exam_id": 1,
            "name": "lorem ipsum dolor",
            "description": "lorem ipsum dolor dolor",
        }
        res = client.patch('/quiz/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_quiz_patch_id_not_found(self, client, init_database):
        token = create_token_admin()
        data = {
            "exam_id": 1,
            "name": "lorem ipsum dolor",
            "description": "lorem ipsum dolor dolor",
        }
        res = client.patch('/quiz/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_quiz_patch_id_admin_business(self, client, init_database):
        token = create_token_admin_business()
        data = {
            "exam_id": 1,
            "name": "lorem ipsum dolor",
            "description": "lorem ipsum dolor dolor",
        }
        res = client.patch('/quiz/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_quiz_delete(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/quiz/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_quiz_delete_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/quiz/100', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_quiz_delete_id_admin_business(self, client, init_database):
        token = create_token_admin_business()
        res = client.delete('/quiz/100', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_quiz_get_all_status_true_examid_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'exam_id', 
            'sort': 'desc'
        }
        res = client.get('/quiz', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_quiz_get_all_status_true_examid_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'exam_id', 
            'sort': 'asc'
        }
        res = client.get('/quiz', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_quiz_get_all_status_true_admin_not_super_academic(self, client, init_database):
        token = create_token_admin_business()
        data={
            'orderby': 'exam_id', 
            'sort': 'asc'
        }
        res = client.get('/quiz', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_quiz_get_all_status(self, client, init_database):
        token = create_token_admin()
        res = client.get('/quiz/all', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200