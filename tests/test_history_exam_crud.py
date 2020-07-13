import json 
from . import app, client, cache, create_token_admin, create_token_mentee, create_token_mentee_user, create_token_mentee_user_1, create_token_mentee_user_not_found, create_token_admin_academic, create_token_admin_business, create_token_admin_council,init_database

class TestHistoryExamCrud():
    def test_history_exam_get_by_token_mentee_exam_id(self, client, init_database):
        token = create_token_mentee()
        data = {
            "exam_id": 1
        }
        res = client.get('/historyexam', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_history_exam_get_by_token_mentee_not_found(self, client, init_database):
        token = create_token_mentee_user_1()
        data = {
            "exam_id": 1
        }
        res = client.get('/historyexam', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_history_exam_get_by_token_mentee_exam_id_livecode(self, client, init_database):
        token = create_token_mentee_user()
        data = {
            "exam_id": 4
        }
        res = client.get('/historyexam', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_history_exam_post_by_token_mentee_and_exam_id(self, client, init_database):
        token = create_token_mentee_user_1()
        data = {
            "exam_id": 2
        }
        res = client.post('/historyexam', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_history_exam_post_exam_not_found(self, client, init_database):
        token = create_token_mentee_user_1()
        data = {
            "exam_id": 5
        }
        res = client.post('/historyexam', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_history_exam_put(self, client, init_database):
        token = create_token_mentee()
        data = {
            "status": True
        }
        res = client.put('/historyexam/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_exam_put_not_found(self, client, init_database):
        token = create_token_mentee()
        data = {
            "status": True
        }
        res = client.put('/historyexam/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_history_exam_patch(self, client, init_database):
        token = create_token_mentee()
        data = {
            "mentee_id": 2,
            "exam_id": 1,
            "score": 80,
            "is_complete": True
        }
        res = client.patch('/historyexam/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_exam_patch_id_not_found(self, client, init_database):
        token = create_token_mentee()
        data = {
            "mentee_id": 2,
            "exam_id": 1,
            "score": 80,
            "is_complete": True
        }
        res = client.patch('/historyexam/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_history_exam_delete(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/historyexam/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_exam_delete_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/historyexam/100', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_history_exam_get_all_status_true_score_desc(self, client, init_database):
        token = create_token_mentee()
        data={
            'orderby': 'score', 
            'sort': 'desc'
        }
        res = client.get('/historyexam/allexam', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_exam_get_all_status_true_score_asc(self, client, init_database):
        token = create_token_mentee()
        data={
            'orderby': 'score', 
            'sort': 'asc'
        }
        res = client.get('/historyexam/allexam', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_exam_get_all_status_true_created_at_desc(self, client, init_database):
        token = create_token_mentee()
        data={
            'orderby': 'created_at', 
            'sort': 'desc'
        }
        res = client.get('/historyexam/allexam', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_exam_get_all_status_true_created_at_asc(self, client, init_database):
        token = create_token_mentee()
        data={
            'orderby': 'created_at', 
            'sort': 'asc'
        }
        res = client.get('/historyexam/allexam', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_exam_get_all_status(self, client, init_database):
        token = create_token_admin()
        res = client.get('/historyexam/all', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200