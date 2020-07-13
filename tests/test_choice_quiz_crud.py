import json 
from . import app, client, cache, create_token_admin, create_token_mentee, create_token_admin_academic, create_token_admin_business, create_token_admin_council,init_database

class TestChoiceQuiz():
    def test_choice_quiz_get_by_id(self, client, init_database):
        token = create_token_admin()
        res = client.get('/choicequiz/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_choice_quiz_by_id_no_access(self, client, init_database):
        token = create_token_admin_business()
        res = client.get('/choicequiz/1', 
                        headers={'Authorization': 'Bearer ' + token}, 
                        content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    def test_choice_quiz_get_by_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.get('/choicequiz/100', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_choice_quiz_post(self, client, init_database):
        token = create_token_admin()
        data={
            "question_id": 1,
            "choice": "Python",
            "is_correct": True,
            "status": True
        }
        res = client.post('/choicequiz', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_choice_quiz_post_admin_business(self, client, init_database):
        token = create_token_admin_business()
        data={
            "question_id": 1,
            "choice": "Python",
            "is_correct": True,
            "status": True
        }
        res = client.post('/choicequiz', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_choice_quiz_post_id_question_not_found(self, client, init_database):
        token = create_token_admin()
        data={
            "question_id": 2,
            "choice": "Python",
            "is_correct": True,
            "status": True
        }
        res = client.post('/choicequiz', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_choice_quiz_put(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": True
        }
        res = client.put('/choicequiz/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_choice_quiz_put_id_not_found(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": True
        }
        res = client.put('/choicequiz/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_choice_quiz_patch(self, client, init_database):
        token = create_token_admin()
        data = {
            "choice": "Python",
            "is_correct": True,
        }
        res = client.patch('/choicequiz/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_choice_quiz_patch_id_not_found(self, client, init_database):
        token = create_token_admin()
        data = {
            "choice": "Python",
            "is_correct": True,
        }
        res = client.patch('/choicequiz/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_choice_quiz_patch_admin_business(self, client, init_database):
        token = create_token_admin_business()
        data = {
            "choice": "Python",
            "is_correct": True,
        }
        res = client.patch('/choicequiz/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404
# ====== masih fail
    def test_choice_quiz_get_all_status_true_choice_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'choice', 
            'sort': 'desc'
        }
        res = client.get('/choicequiz', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_choice_quiz_get_all_status_true_choice_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'choice', 
            'sort': 'asc'
        }
        res = client.get('/choicequiz', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_choice_quiz_get_all_status_true_createdat_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'created_at', 
            'sort': 'desc'
        }
        res = client.get('/choicequiz', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_choice_quiz_get_all_status_true_question_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'created_at', 
            'sort': 'asc'
        }
        res = client.get('/choicequiz', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_choice_quiz_get_all_admin_business(self, client, init_database):
        token = create_token_admin_business()
        data={
            'orderby': 'created_at', 
            'sort': 'asc'
        }
        res = client.get('/choicequiz', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_choice_quiz_get_all_status(self, client, init_database):
        token = create_token_admin()
        res = client.get('/choicequiz/all', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200
   
    def test_choice_quiz_delete(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/choicequiz/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_choice_quiz_delete_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/choicequiz/100', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_choice_quiz_delete_admin_business(self, client, init_database):
        token = create_token_admin_business()
        res = client.delete('/choicequiz/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404